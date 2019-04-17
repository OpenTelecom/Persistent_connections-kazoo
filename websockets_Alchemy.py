import websockets as w
import asyncio
import json as j
from data_alchemy import insert_data


from websockets import ConnectionClosed
from config import *


def jsonify(d):
    """
    jsonify a message

    :param d: a dict to turn into a json file
    """
    jsonfied = j.dumps(d)
    return jsonfied


def consumer_device(data):
    item_type = data.get('type')
    item_id = data.get('id')
    account_id = data.get('account_id')
    print(item_type, item_id, account_id)
    insert_data(item_type, account_id, item_id, AUTH_TOKEN)


def consumer_user(data):
    item_type = data.get('type')
    item_id = data.get('id')
    account_id = data.get('account_id')
    print(item_type, item_id, account_id)
    insert_data(item_type, account_id=account_id, item_id=item_id, auth=AUTH_TOKEN)


def consumer_accounts(data):
    item_type = data.get('type')
    item_id = data.get('id')
    account_id = data.get('account_id')
    insert_data(item_type, account_id, item_id, AUTH_TOKEN)


def consume_call(data):
    dir_inbound = data.get('call_direction')
    callee = data.get('callee_id_name')
    caller = data.get('caller_id_name')
    duration = data.get('duration_seconds')
    call_vars = data.get('custom_channel_vars')
    interaction_id = call_vars.get('call_interaction_id')
    account_id = call_vars.get('account_id')
    print(f'callee: {callee}, caller: {caller}, duration: {duration}, interaction_id: {interaction_id}, account_id: {account_id}')

    if dir_inbound == 'inbound':
        print('inbound in, sending data to database')
        inbound = call_vars.get('owner_id')
        insert_data('call', account_id, interaction_id, AUTH_TOKEN, inbound=inbound, callee=callee, caller=caller, duration=duration)
    elif dir_inbound == 'outbound':
        print('outbound in, sending data to database')
        inbound = call_vars.get('owner_id')
        insert_data('call', account_id, interaction_id, AUTH_TOKEN, outbound=inbound, callee=callee, caller=caller, duration=duration)


async def consumer(event):
    """
    consumer code that prints the notifications from messages sent by the websocket connection
    - does something with the messages sent by server

    """

    event = j.loads(event)

    print(j.dumps(event, indent=2, sort_keys=True))
    print('*' * 100)
    data = event.get('data')
    print('in if statement')

    if 'custom_channel_vars' in data:
        if data.get('event_name') == 'CHANNEL_DESTROY':
            print('sending data to consumer_calls')
            consume_call(data)
    elif data.get('type') == 'user':
        consumer_user(data)
    elif data.get('type') == 'device':
        consumer_device(data)
    else:
        consumer_accounts(data)


async def hello():
    """
    Start connection to blackhole over 5555
    :return:
    """
    print('trying to connect')
    async with w.connect(f"ws://{KAZOO_HOST}:5555") as ws:
        print('connected')
        """
        Devices
        """
        await ws.send(jsonify(WEBSOCKET_CreateDevice))
        try:
            response = await ws.recv()
            print(response)

        except ConnectionClosed:
            print('closed connection')
        """
        User
        """
        await ws.send(jsonify(WEBSOCKET_CreateUser))
        try:
            response = await ws.recv()
            print(response)

        except ConnectionClosed:
            print('closed connection')
        """
        Channel Create
        """

        await ws.send(jsonify(WEBSOCKET_Channel_Create))
        try:
            response = await ws.recv()
            print(response)

        except ConnectionClosed:
            print('closed connection')

        """
        Channel Destroy
        """
        await ws.send(jsonify(WEBSOCKET_Channel_Destroy))
        try:
            response = await ws.recv()
            print(response)

        except ConnectionClosed:
            print('closed connection')

        """
        consumer code that handles the messages sent by the server
        
        """
        async for messages in ws:
            await consumer(messages)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())
