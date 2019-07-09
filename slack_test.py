import os
import slack


def send_slack_msg():
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    response = client.chat_postMessage(
        channel='#test',
        text="Hello world!")
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"


# zookeper shards and replicas checks here
def check_solr_cloud():
    return


send_slack_msg()
