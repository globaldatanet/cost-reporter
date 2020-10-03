import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    client = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')
    first_day_of_month = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    results = client.get_cost_and_usage(
        TimePeriod={
            'Start': first_day_of_month,
            'End': today
        },
        Granularity='MONTHLY',
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
    print(json.dumps(results, indent=4))

lambda_handler({}, {})