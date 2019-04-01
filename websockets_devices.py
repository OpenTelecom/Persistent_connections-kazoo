import websockets as w
import asyncio
import json as j

from websockets import ConnectionClosed
import kazoo_put as kp
from data_alchemy import insert_data


"""
Makes second connection to kazoo for user creation
"""


# Global Variables
HOST = '18.218.219.1'
auth_token = kp.get_auth_token()
acc_id = kp.get_acc_id()


def jsonify(d):
    """
    jsonify a message

    :param d: a dict to turn into a json file
    """
    jsonfied = j.dumps(d)
    return jsonfied


# subscription message to crossbar with single binding
message = {
    'action': 'subscribe',
    'auth_token': auth_token,
    'request_id': acc_id,
    'data': {
        'account_id': acc_id,
        'binding': 'object.doc_created.device'
    }
}


async def consumer(event):
    """
    consumer code that prints the notifications from messages sent by the websocket connection
    - does something with the messages sent by server

    """
    event = j.loads(event)
    data = event['data']
    item_type = data.get('type')
    item_id = data.get('id')
    account_id = data.get('account_id')
    print(item_type, item_id, account_id)
    print()
    insert_data(item_type, account_id, item_id, auth_token)

    # item = kp.get_items(item_type, account_id, item_id, auth=auth_token)
    # print(item)
    # data = item['data']
    # print(data)
    # device_type = data.get('device_type')
    # owner_id = data.get('owner_id')
    # name = data.get('name')
    # print('name , type, owner_id', name, device_type, owner_id)


async def hello():
    """
    Start connection to blackhole over 5555
    :return:
    """
    print('trying to connect')
    async with w.connect(f"ws://{HOST}:5555") as ws:
        print('connected')
        await ws.send(jsonify(message))
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
