import websockets as w
import asyncio
import json as j
from data_alchemy import insert_data


from websockets import ConnectionClosed
import kazoo_put as kp


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

message1 = {
    'action': 'subscribe',
    'auth_token': auth_token,
    'request_id': acc_id,
    'data': {
        'account_id': acc_id,
        'binding': 'call.CHANNEL_CREATE.*'
    }
}

message2 = {
    'action': 'subscribe',
    'auth_token': auth_token,
    'request_id': acc_id,
    'data': {
        'account_id': acc_id,
        'binding': 'call.CHANNEL_DESTROY.*'
    }
}


async def consumer(event):
    """
    consumer code that prints the notifications from messages sent by the websocket connection
    - does something with the messages sent by server

    """

    event = j.loads(event)
    print(j.dumps(event, indent=2, sort_keys=True))

    data = event['data']
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
        # print(inbound)
        insert_data('call', account_id, interaction_id, auth_token, inbound=inbound, callee=callee, caller=caller, duration=duration)
    elif dir_inbound == 'outbound':
        print('outbound in, sending data to database')
        inbound = call_vars.get('owner_id')
        # print(inbound)
        insert_data('call', account_id, interaction_id, auth_token, outbound=inbound, callee=callee, caller=caller, duration=duration)


async def hello():
    """
    Start connection to blackhole over 5555
    :return:
    """
    print('trying to connect')
    async with w.connect(f"ws://{HOST}:5555") as ws:
        print('connected')
        await ws.send(jsonify(message2))
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
