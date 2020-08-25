# for listening to websockets messages
import asyncio
import websockets
# for retrieving API tokens from the AlphaHub server
import requests
from creds import email, password

import json

SERVER = { "hostname": "alphahub.us" }
IDS = [14, 16, 17]

def sockets_uri(server):
    return "wss://" + server["hostname"]

def http_uri(server):
    return "https://" + server["hostname"]

def authenticate():
    url = http_uri(SERVER) + "/api/v1/session"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'user[email]': email, 'user[password]': password}
    response = requests.post(url, data, headers=headers)
    json = response.json()
    return json["data"]

async def handle_messages(websocket):
    async for json_message in websocket:
        message = json.loads(json_message)
        channel = message[2]
        topic = message[3]
        contents = message[4]
        if contents["open"]:
            print("new open signals on", channel, ":", contents["open"])
        if contents["close"]:
            print("new close signals on", channel, ":", contents["close"])
        if not contents["open"] and not contents["close"]:
            print("channel: ", channel)
            print("contents: ", contents)


async def send_join_messages(websocket, ids):
    for id in ids:
        join_message = [None, None, "algorithms:" + str(id), "phx_join", {}]
        await websocket.send(json.dumps(join_message))
        await websocket.recv()

async def consumer(credentials, ids):
    url = sockets_uri(SERVER) + "/socket/websocket?api_token=" + credentials["token"] + "&vsn=2.0.0"
    async with websockets.connect(url) as websocket:
        await send_join_messages(websocket, ids)
        await handle_messages(websocket)

print("Retrieving tokens...")
tokens = authenticate()
print("Tokens retrieved")

print("listening for new signals...")
loop = asyncio.get_event_loop()
loop.run_until_complete(consumer(tokens, IDS))
loop.run_forever()
