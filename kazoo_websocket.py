import websockets as w
import asyncio
import json as j

from websockets import ConnectionClosed
from config import WEBSOCKET_Channel_Create, KAZOO_HOST


def jsonify(d):
    """
    jsonify a message

    :param d: a dict to turn into a json file
    """
    jsonfied = j.dumps(d)
    return jsonfied


# subscription message to crossbar with single binding


async def consumer(event):
    """
    consumer code that prints the notifications from messages sent by the websocket connection
    - does something with the messages sent by server

    """

    event = j.loads(event)
    print(j.dumps(event, indent=2, sort_keys=True))

    data = event['data']
    call_vars = data.get('custom_channel_vars')
    owner_id = call_vars.get('owner_id')
    interaction_id = call_vars.get('call_interaction_id')
    print(data)
    print('-' * 1000)
    print(owner_id)
    print(interaction_id)
    # item_type = data.get('type')
    # item_id = data.get('id')
    # account_id = data.get('account_id')

    # print(f'item_type: {item_type}, item_id: {item_id}, account_id: {account_id}')


async def hello():
    """
    Start connection to blackhole over 5555
    :return:
    """
    print('trying to connect')
    async with w.connect(f"ws://{KAZOO_HOST}:5555") as ws:
        print('connected')
        await ws.send(jsonify(WEBSOCKET_Channel_Create))
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
