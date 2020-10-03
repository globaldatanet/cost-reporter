import boto3
from datetime import datetime, timedelta
import json
import stacked_bar

DAYS = 10


def get_daily_cost():
    """ Returns the spend for each service
    """
    client = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')
    # first_day_of_month = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=DAYS)).strftime('%Y-%m-%d')
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

    # Prep the data for the graphing
    # Get the list of services
    services = [x["Keys"][0] for x in results[0]["Groups"]]
    #services = ['AWS Transfer Family', 'AWS Lambda', 'Amazon Relational Database Service', 'Amazon DynamoDB']
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

    print(json.dumps(daily_cost, indent=4))
    return daily_cost


def lambda_handler(event, context):
    daily_cost = get_daily_cost()

    # Find the biggest spenders
    total_cost = []
    for service in daily_cost.keys():
        total_cost.append((service, sum(daily_cost[service])))
    total_cost = sorted(total_cost, key = lambda x: x[1], reverse=True)

    top_5 = [x[0] for x in total_cost][0:5]
    the_rest = [x[0] for x in total_cost][5:]
    #print(top_5)

    graph_data = {}
    # add top-5
    for service in top_5:
        graph_data[service] = daily_cost[service]
    # add the rest
    graph_data["Other"] = [0 for x in range(DAYS)]
    for service in the_rest:
        graph_data["Other"] = [x + y for x, y in zip(graph_data["Other"], daily_cost[service])]
    
    print(graph_data)

    for service in graph_data.keys():
        

    stacked_bar.draw_bars(graph_data)

    #print(json.dumps(results, indent=4))


lambda_handler({}, {})