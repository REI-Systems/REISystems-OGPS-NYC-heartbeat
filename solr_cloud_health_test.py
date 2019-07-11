#!/usr/bin/env python

import os

from slackclient import SlackClient
import requests
from inc import ReiSlack


def get_solr_cloud_status():
    solr_endpoints = os.environ['SOLR_ENDPOINTS'].split(',')

    # http://sdw5.reisys.com:18983/solr/admin/collections?action=CLUSTERSTATUS&wt=json
    for endpoint in solr_endpoints:
        url = "http://" + endpoint + "/solr/admin/collections?action=CLUSTERSTATUS&wt=json"
        response = requests.get(url=url)
        if response:
            return response.json()
    raise ValueError('could not reach any SOLR endpoint')


def main():
    try:
        all_good = True
        bad_nodes = dict()
        down_msg = ''
        r = get_solr_cloud_status()
        msg = "ALL GOOD: "
        for collection, collection_info in r['cluster']['collections'].items():
            for shard, shard_info in collection_info['shards'].items():
                if "active" != shard_info['state']:
                    down_msg += "\n :scream: '{0}' state: '{1}' (core '{2}')".format(shard, shard_info['state'],
                                                                                     collection)
                    all_good = False
                for replica, replica_info in shard_info['replicas'].items():
                    if "active" != replica_info['state']:
                        all_good = False
                        if replica_info['base_url'] not in bad_nodes.keys():
                            bad_nodes[replica_info['base_url']] = replica_info['state']
            msg += "\n * " + collection
        if all_good:
            ReiSlack.send(msg)
        else:
            down_msgs = list()
            for k, v in bad_nodes.items():
                down_msgs.append(":cry: {0} state: '{1}'".format(k, v))
            ReiSlack.send(down_msg + "\n".join(down_msgs), "error")
    except ValueError as err:
        ReiSlack.send("Fatal: {0}".format(err), "error")


if __name__ == '__main__':
    main()
