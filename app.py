import asyncio
import logging
import json
import secrets
import signal
import os
import sys

from websockets.asyncio.server import broadcast, serve

GROUPS = {}
COLORS = ['#e41a1c', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']

async def error(websocket, message):
    """
    Send an error message.
    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def send_receive(websocket, device_key, devices, connected):
    """
    Receive and process location from a device.
    """
    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "position" or event["type"] == "message"
        if event["type"] == "position":
            lat = event["lat"]
            lon = event["lon"]
            direction = event["dir"]
            speed = event["speed"]
            
            devices[device_key]["lat"] = lat
            devices[device_key]["lon"] = lon
            devices[device_key]["dir"] = direction
            devices[device_key]["speed"] = speed
            
            event = {
                "type": "positions",
                "devices": devices
            }
            broadcast(connected, json.dumps(event))
        elif event["type"] == "message":
            content = event["content"]
            
            event = {
                "type": "message",
                "device": device_key,
                "content": content,
            }
            broadcast(connected, json.dumps(event))

async def create(websocket, user_name):
    """
    Handle a connection from the device creating a new group.
    """
    group_key = secrets.token_urlsafe(12)
    device_key = secrets.token_urlsafe(12)

    devices = {}
    devices[device_key] = { "user_name": user_name, "user_color": COLORS[0] }
    connected = {websocket}

    GROUPS[group_key] = devices, connected

    try:
        print(f"Group created by device {device_key} with access token {group_key}...")
        # Send the secret group access token as well as the device token.
        event = {
            "type": "created",
            "group": group_key,
            "device": device_key,
        }
        await websocket.send(json.dumps(event))
        # Receive and process the device(s) position
        await send_receive(websocket, device_key, devices, connected)
    finally:
        print(f"Device {device_key} left group with access token {group_key}...")
        connected.remove(websocket)
        del devices[device_key]
        if len(connected) == 0:
            print(f"Removing emptied group with access token {group_key}...")
            del GROUPS[group_key]


async def join(websocket, user_name, group_key):
    """
    Handle a connection from devices wanting to join an existing group.
    """
    try:
        devices, connected = GROUPS[group_key]
    except KeyError:
        print("Group not found, not entering...")
        await error(websocket, "Group not found.")
        return

    device_key = secrets.token_urlsafe(12)
    
    # Register the device joining the group.
    devices[device_key] = { "user_name": user_name, "user_color": COLORS[len(devices) % 5] }
    connected.add(websocket)
    try:
        print(f"Device {device_key} joined group with access token {group_key}...")
        # Send the secret group access token as well as the device token.
        event = {
            "type": "joined",
            "group": group_key,
            "device": device_key,
        }
        await websocket.send(json.dumps(event))
        # Send the current device(s) position
        event = {
            "type": "positions",
            "devices": devices
        }
        await websocket.send(json.dumps(event))
        # Receive and process the device(s) position
        await send_receive(websocket, device_key, devices, connected)
    finally:
        print(f"Device {device_key} left group with access token {group_key}...")
        connected.remove(websocket)
        del devices[device_key]
        if len(connected) == 0:
            print(f"Removing emptied group with access token {group_key}...")
            del GROUPS[group_key]


async def handler(websocket):
    """
    Handle a connection request.
    """
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "join" or event["type"] == "create"

    if event["type"] == "join":
        await join(websocket, event["user"], event["group"])
    elif event["type"] == "create":
        await create(websocket, event["user"])

class SkipHandshakeErrorsHandler(logging.StreamHandler):
    def handle(self, record):
        if not record.msg == "opening handshake failed":
            super().handle(record)

async def main():
    logging.getLogger("websockets").addHandler(SkipHandshakeErrorsHandler(sys.stdout))
    print("Launching server...")
    
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
