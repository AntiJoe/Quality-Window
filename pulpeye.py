# pulpeye

import json
import time
import socket
from datetime import datetime
from pulpeye_secrets import server_list
hostname = socket.gethostname()

packet_string = """
{
    "meta":{
        "packet_time": "2017-12-22 9:05:26",
        "host": "operator",
        "records": 4
        },
    "samples": [
         {
            "name": "Line 1",
            "SamplePoint": 1,
            "sampletime": "2017-12-22 8:05:26",
            "batchID": 1,
            "csf": 130,
            "fl": 1.56,
            "shives_sum": 412
         },
         {
            "name": "Line 3",
            "SamplePoint": 3,
            "sampletime": "2017-12-22 8:05:26",
            "batchID": 2,
            "csf": 135,
            "fl": 1.59,
            "shives_sum": 823
        },
         {
            "name": "Line 2",
            "SamplePoint": 2,
            "sampletime": "2017-12-22 8:06:26",
            "batchID": 3,
            "csf": 140,
            "fl": 1.66,
            "shives_sum": 367
        },
        {
            "name": "Rejects",
            "SamplePoint": 4,
            "sampletime": "2017-12-22 8:06:26",
            "batchID": 5,
            "csf": 140,
            "fl": 1.71,
            "shives_sum": 67
        }
    ]
}
"""

packet_json = json.loads(packet_string)
samples = packet_json['samples']
meta = packet_json['meta']

now = datetime.now()

class pulpeye():
    def __init__(self):
        sql_ip = '192.168.2.205'
        meta['host'] = hostname

    def connect_pulpeye(self):
        pass

    def meta_update(self):
        meta['packet_time'] = now

    def add_sample(self):
        pass

    def build_packet(self):
        pass

    def send_packet(self):
        pass


