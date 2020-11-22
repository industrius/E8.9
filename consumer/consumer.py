"""
Consumer - по сути "транслятор" сообщений из очереди NSQ
на адрес API функции add_result Django.
"""

import os
import json
import nsq
import requests

NSQ_ADDR = os.environ.get("NSQ_ADDR")
POST_ADDR = os.environ.get("POST_ADDR")

def handler(message):
    requests.post("http://" + POST_ADDR + "/add_result", data=json.loads(message.body.decode()))
    # print("NSQ translate: ", message.body.decode())
    return True

r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=NSQ_ADDR, topic='bg_worker', channel='consumer_channel', lookupd_poll_interval=15)

if __name__ == '__main__':
    # print("NSQ Started")
    nsq.run()