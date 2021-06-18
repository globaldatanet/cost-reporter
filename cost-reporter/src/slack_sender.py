import os

import boto3
import slack


def get_token() -> str:
    ssm = boto3.client("ssm")

    return ssm.get_parameter(
        Name=os.environ["SLACK_TOKEN_PARAMETER"],
        WithDecryption=True
    )["Parameter"]["Value"]


def send_image(filename: str, slack_channel: str) -> None:
    slacker = slack.WebClient(token=get_token())
    slacker.files_upload(channels=slack_channel, file=filename, title="Cost report")
