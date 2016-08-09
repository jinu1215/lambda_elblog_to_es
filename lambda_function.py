from __future__ import print_function

import boto3
import re

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import configs

#ES_HOST=<your elasticsearch host>
#ES_PORT=80
#ES_BULK_CHUNK_SIZE=1000
ELB_KEYS = ["timestamp", "elb", "client_ip", "client_port",
            "backend_ip", "backend_port", "request_processing_time",
            "backend_processing_time", "response_processing_time",
            "elb_status_code", "backend_status_code", "received_bytes",
            "sent_bytes", "request_method", "request", "user_agent",
            "ssl_cipher", "ssl_protocol"]

ELB_REGEX = '^(.[^ ]+) (.[^ ]+) (.[^ ]+):(\\d+) (.[^ ]+):(\\d+) (.[^ ]+) (.[^ ]+) (.[^ ]+) (.[^ ]+) (.[^ ]+) (\\d+) (\\d+) \"(\\w+) (.+)\" \"(.+)\" (.[^ ]+) (.[^ ]+)'
ELB_R = re.compile(ELB_REGEX)

def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    s3 = boto3.client("s3")
    obj = s3.get_object(
        Bucket=bucket,
        Key=key
    )
    dirs = key.split('/')
    if dirs[2] == "elasticloadbalancing":
        index = ("awslogs-elb-%s" % (datetime.strftime(datetime.now(), "%Y%m%d")))
        R = ELB_R
    else:
        index = ("awslogs-%s" % (datetime.strftime(datetime.now(), "%Y%m%d")))
        R = ELB_R
    body = obj["Body"].read()

    es = Elasticsearch(host=configs.ES_HOST, port=configs.ES_PORT)
    actions = []
    elb_name = ""

    for line in body.strip().split("\n"):
        match = R.match(line)
        if not match:
            continue

        values = match.groups(0)
        if not elb_name:
            elb_name = values[1]
        doc = dict(zip(ELB_KEYS, values))

        actions.append({"_index": index, "_type": elb_name, "_source": doc})

        if len(actions) > configs.ES_BULK_CHUNK_SIZE:
            helpers.bulk(es, actions)
            actions = []

    if len(actions) > 0:
        helpers.bulk(es, actions)
