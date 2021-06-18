import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import boto3

import slack_sender
import stacked_bar


def get_daily_cost() -> Dict[str, List[float]]:
    """ Return the spend for each service together by day
    """
    days = int(os.environ["DAYS"])

    today = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # Get daily spend
    client = boto3.client('ce')
    results = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': today
        },
        Granularity='DAILY',
        Metrics=[
            'AmortizedCost',
        ],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )["ResultsByTime"]

    # Prep the data for the graphing: Get the list of services
    services = [x["Keys"][0] for x in results[0]["Groups"]]
    daily_cost = {service: [] for service in services}
    for service in services:
        for day in results:
            found_service = False
            for group in day["Groups"]:
                if service in group["Keys"]:
                    daily_cost[service].append(float(group["Metrics"]["AmortizedCost"]["Amount"]))
                    found_service = True
                    break
            # Fill up a 0 if service doesnt have cost for that day
            if not found_service:
                daily_cost[service].append(0)

    return daily_cost


def trigger_notification(graph_data: Dict[str, List[float]]) -> bool:
    """ Determine whether or not a notification should be send
    """
    should_send = True

    total_cost_today = 0
    total_cost_yesterday = 0
    for service in graph_data.keys():
        total_cost_today += graph_data[service][-1]
        total_cost_yesterday += graph_data[service][-2]
    logging.info(f"Total cost today: {total_cost_today}")
    logging.info(f"Total cost yesterday: {total_cost_yesterday}")

    only_notify_on_increase = os.environ["ONLY_NOTIFY_ON_INCREASE"].lower()
    if only_notify_on_increase == "true":
        if total_cost_today < total_cost_yesterday:
            logging.info("Not sending, since cost did not increase and I should only notify on increase.")
            should_send = False

    min_daily_cost = int(os.environ["MIN_DAILY_COST"])
    if min_daily_cost > total_cost_today:
        should_send = False
        logging.info("Minimal daily cost not exceeded!")
    else:
        logging.info("Minimal daily cost exceeded!")

    return should_send


def get_highest_spenders(daily_cost: Dict[str, List[float]], number: int) -> Tuple[List[str], List[str]]:
    """ Divide the cost between the {number} highest spending services and the rest
    """
    # Summarize the cost and find the biggest spenders
    total_cost = [(service, sum(daily_cost[service])) for service in daily_cost.keys()]
    total_cost = sorted(total_cost, key=lambda x: x[1], reverse=True)

    services_by_cost = [x[0] for x in total_cost]
    highest_spenders = services_by_cost[0:number]
    the_rest = services_by_cost[number:]

    if len(highest_spenders) < number:
        logging.info(f"Notice: I was looking for the top {number} of spending services, but there are " +
                     f"only {len(highest_spenders)}. Will continue anyway.")

    logging.info(f"Top {number} services:" + str(highest_spenders))

    return highest_spenders, the_rest


def compile_graph_data(daily_cost: Dict[str, List[float]], highest_spenders: List[str],
                       the_rest: List[str]) -> Dict[str, List[float]]:
    days = int(os.environ["DAYS"])
    graph_data = {}  # type: Dict[str, List[float]]

    # add the highest spenders
    for service in highest_spenders:
        graph_data[service] = daily_cost[service]

    # add the rest
    graph_data["Other"] = [0] * days
    for service in the_rest:
        graph_data["Other"] = [x + y for x, y in zip(graph_data["Other"], daily_cost[service])]

    return graph_data


def lambda_handler(event: Dict, _) -> None:
    # Configure logging
    level = os.environ.get("LOG_LEVEL", "INFO")
    logging.getLogger().setLevel(level)

    daily_cost = get_daily_cost()

    # determine the top 5 spending services
    (highest_spenders, the_rest) = get_highest_spenders(daily_cost, 5)

    graph_data = compile_graph_data(daily_cost, highest_spenders, the_rest)

    logging.info("Generating the graph...")
    stacked_bar.draw_bars(graph_data, f"{os.environ['TITLE']} (last {os.environ['DAYS']} days)")
    logging.info("Graph generated")

    # Send the report if necessary
    if trigger_notification(graph_data):
        logging.info("Sending message")
        slack_sender.send_image("/tmp/image.png", os.environ["TARGET_CHANNEL"])
    else:
        logging.info("Not sending the message due to trigger configuration.")
