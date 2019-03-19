import websockets as w
import asyncio
import json as j

from websockets import ConnectionClosed
import kazoo_put as kp

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
        'binding': 'object.doc_created.user'
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
    item = kp.get_items(item_type, account_id, item_id, auth=auth_token)
    print(item)


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
