#!/usr/bin/env python

import os

from slackclient import SlackClient


def send(msg="no msg", rsp="ok"):
    channel = os.environ['SLACK_CHANNEL']

    if "ok" == rsp:
        if 'SKIP_OK_MESSAGES' in os.environ and os.environ['SKIP_OK_MESSAGES']:
            return
        if 'SLACK_OK_CHANNEL' in os.environ and os.environ['SLACK_OK_CHANNEL']:
            channel = os.environ['SLACK_OK_CHANNEL']
        msg = ":white_check_mark: " + msg
    else:
        msg = ":bomb: " + msg

    sc = SlackClient(token=os.environ['SLACK_API_TOKEN'])
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )
