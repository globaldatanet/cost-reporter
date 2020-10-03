import boto3
from datetime import datetime, timedelta
import json
import stacked_bar

def lambda_handler(event, context):
    client = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')
    first_day_of_month = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    results = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date, #first_day_of_month,
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

    # TODO find the biggest spenders so far. for this, issue a query and sort by MONTHLY

    # Prep the data for the graphing
    # Get the list of services
    #services = [x["Keys"][0] for x in results[0]["Groups"]]
    services = ['AWS Transfer Family', 'AWS Lambda', 'Amazon Relational Database Service', 'Amazon DynamoDB']
    graph_data = {service: [] for service in services}
    for service in services:
        for day in results:
            found_service = False
            for group in day["Groups"]:
                if service in group["Keys"]:
                    graph_data[service].append(float(group["Metrics"]["AmortizedCost"]["Amount"]))
                    found_service = True
                    break
            # Fill up a 0 if service doesnt have cost for that day
            if not found_service:
                graph_data[service].append(0)

    #print(json.dumps(graph_data, indent=4))
    stacked_bar.draw_bars(graph_data)
    #print(json.dumps(results, indent=4))


lambda_handler({}, {})