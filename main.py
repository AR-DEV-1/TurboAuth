# and then run the main code

from flask import Flask

from replit import db as rdb
import os
os.system("pip install scratchattach")
import scratchattach as sa
import string
import random

PROJECT_ID = 721834570
twkeys = dict(rdb["twkeys"])

session = sa.Session(os.environ["session"], username="TimMcCool")
cloud = session.connect_cloud(project_id=PROJECT_ID)
client = sa.CloudRequests(cloud)

twcloud = sa.TwCloudConnection(project_id=PROJECT_ID)
twclient = sa.TwCloudRequests(twcloud)

def random_string(len):
    return ''.join((random.choice(string.ascii_letters+string.digits+"-_") for x in range(len)))
    
@client.event
def on_request(request):
    print("TW Auth received a request")

@client.request
def get():
    if client.get_requester() not in twkeys:
        return _recreate()
    return twkeys[client.get_requester()]

def _recreate():
    global twkeys
    twkeys[client.get_requester()] = random_string(15)
    rdb["twkeys"] = twkeys
    return twkeys[client.get_requester()]

@client.request
def recreate():
    return _recreate()
    
@twclient.request
def validate(key):
    if key in list(twkeys.values()):
        twkeys_flipped = dict(zip(twkeys.values(), twkeys.keys()))
        return twkeys_flipped[key]
    else:
        return "-"
    
app = Flask(__name__)

def run_server():
    app.run(host='0.0.0.0', port=5000)

import threading
server_thread = threading.Thread(target=run_server)
server_thread.start()

client.run(thread=True)
twclient.run()
