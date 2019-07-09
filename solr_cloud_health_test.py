#!/usr/bin/env python

import os

from slackclient import SlackClient
import requests


def send_slack_msg(msg="no msg", rsp="ok"):
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


def get_solr_cloud_status():
    solr_endpoints = os.environ['SOLR_ENDPOINTS'].split(',')
    for endpoint in solr_endpoints:
        url = "http://" + endpoint + "/solr/admin/collections?action=CLUSTERSTATUS&wt=json"
        response = requests.get(url=url)
        if response:
            return response.json()
    raise ValueError('could not reach any SOLR endpoint')


def main():
    try:
        all_good = True
        r = get_solr_cloud_status()
        msg = "ALL GOOD: "
        for collection, collection_info in r['cluster']['collections'].items():
            for shard, shard_info in collection_info['shards'].items():
                if "active" != shard_info['state']:
                    all_good = False
                    send_slack_msg(
                        "Error: core '{0}' shard '{1}' state '{2}'".format(collection, shard, shard_info['state']),
                        "error"
                    )
                for replica, replica_info in shard_info['replicas'].items():
                    if "active" != replica_info['state']:
                        all_good = False
                        send_slack_msg(
                            "Warning: core '{0}' shard '{1}' replica '{2}' state '{3}'".format(collection, shard,
                                                                                               replica,
                                                                                               replica_info['state']),
                            "error"
                        )
            msg += "\n * " + collection
        if all_good:
            send_slack_msg(msg)
        else:
            send_slack_msg('Check errors found', "error")
    except ValueError as err:
        send_slack_msg("Fatal: {0}".format(err), "error")
    # except:
    #     send_slack_msg("Fatal: {0}".sys.exc_info()[0], "error")
    #     print("Unexpected error:", sys.exc_info()[0])
    #     raise


if __name__ == '__main__':
    main()
