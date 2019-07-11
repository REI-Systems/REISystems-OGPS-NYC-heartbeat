#!/usr/bin/env python
import random
from urllib import request

from inc import ReiSlack
from solr_cloud_health_test import get_solr_cloud_status


def main():
    instances = list()
    try:
        r = get_solr_cloud_status()
        for collection, collection_info in r['cluster']['collections'].items():
            for shard, shard_info in collection_info['shards'].items():
                if "active" == shard_info['state']:
                    for replica, replica_info in shard_info['replicas'].items():
                        if "active" == replica_info['state']:
                            instances.append(replica_info['base_url'])

        if len(instances):
            victim = random.choice(instances)
            ReiSlack.send('CMonkey: killing ' + victim, "error")
            request.urlopen(victim + "/checkbook_nycha_dev.public.solr_nycha/select/?q=*:*&facet=true" +
                            "facet.limit=-1&facet.field=contract_number&facet.field=id")
    except ValueError as err:
        ReiSlack.send("Fatal: {0}".format(err), "error")


if __name__ == '__main__':
    main()
