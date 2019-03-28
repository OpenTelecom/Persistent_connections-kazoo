import websockets as w
import asyncio
import json as j
from user import User
from datetime import date

from websockets import ConnectionClosed
import kazoo_put as kp
from base import Session, engine, Base


# Global Variables
HOST = '18.218.219.1'
auth_token = kp.get_auth_token()
acc_id = kp.get_acc_id()
object_id = ''


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


def create_id():
    return object_id


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

    print(item_type)

    Base.metadata.create_all(engine)
    session = Session()

    if item_type == 'user':
        item = kp.get_items(item_type, account_id, item_id, auth=auth_token)
        print(item)
        data = item['data']
        user_name = data['caller_id']['internal']['name']
        email = data.get('email')
        user = User(item_id, user_name, date(2015, 4, 2), 3, email)
        session.add(user)

    session.commit()
    session.close()

    # global object_id
    # object_id = data.get('id')
    # print('this is object id', object_id)

    # item = kp.get_items(item_type, account_id, item_id, auth=auth_token)
    # print(item)

    # uid = insert.insert_user(user_name, item, item_id)
    # print(uid)


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
