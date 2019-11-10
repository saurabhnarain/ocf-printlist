import functools
import os
import sys
import redis
from flask import Flask
from flask import render_template

redis_connection = functools.partial(
    redis.StrictRedis,
    host='broker',
    port=6378,
    ssl=True,
    db=0,
    password=None
)

def subscribe(host, password, *channels):
    rc = redis_connection(host=host, password=password)
    sub = rc.pubsub(ignore_subscribe_messages=True)
    sub.subscribe(channels)
    return sub

printer_dict = {'logjam': ['test_user1'], 'pagefault': ['test_user2'], 'papercut': ['test_user3']}

def monitor_printer(printer):
    host, password = 'broker.ocf.berkeley.edu', '###'

    s = subscribe(host, password, 'printer-' + printer)
    while True:
        message = s.get_message()
        if message and 'data' in message:
            user_list = message['data'].decode(encoding='UTF-8').replace('\n', ' ')
            print(user_list) #need to see what the output is like

if __name__ == '__main__':
    main()

app = Flask(__name__)

@app.route('/')
def home():
    return printer_dict