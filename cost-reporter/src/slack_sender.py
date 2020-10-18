import slack
import os
import boto3
import pathlib


def get_token():
    ssm = boto3.client("ssm")

    return ssm.get_parameter(
        Name=os.environ["SLACK_TOKEN_PARAMETER"],
        WithDecryption=True
    )["Parameter"]["Value"]


def send_image(filename, slack_channel):
    filepath = pathlib.Path(filename).resolve()

    slacker = slack.WebClient(token=get_token())
    slacker.files_upload(channels=slack_channel, file=str(filepath), title="Cost report")
