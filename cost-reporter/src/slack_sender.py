import slack
import json
import os


def pureimg(data):
    data = '[{"text": "", "image_url": "' + data + '"}]'
    data = [json.loads(data[1:-1])]

    return data


def send_image(filename, slack_channel):
    slacker = slack.WebClient(token='your-token-here')

    payoff = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

    response = slacker.files_upload(channel='#theta', file=payoff)
    payoff = response['file']['permalink']

    response = slacker.chat_postMessage(
        channel='#channel_name',
        text="Sample Text",
        username='Bot name',
        attachments=pureimg(payoff),
        icon_emoji=':rocket:')