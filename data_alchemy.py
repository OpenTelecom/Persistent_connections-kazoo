
from base import Session, engine, Base
import kazoo_put as kp
from user import User
from device import Device
from account import Account
from datetime import datetime


def insert_data(item_type, account_id, item_id, auth):

    Base.metadata.create_all(engine)
    session = Session()

    # def __init__(self, id_id, name, create_date, no_devices, email, account):
    def create_user():
        print('Creating Users WOWOWOWOWOWO')
        item_user = kp.get_items(item_type=item_type, account_id=account_id, item_id=item_id, auth=auth)
        print('in data_alchemy', item_user)

        data = item_user['data']
        if data.get('priv_level') == 'admin':
            user_name = 'admin'
            email = 'master@local.com'
        else:
            user_name = data['caller_id']['internal']['name']
            email = data.get('email')
        account = session.query(Account).get(account_id)
        user = User(item_id, user_name, datetime.now(), 1, email, account)
        session.add(user)

    # def __init__(self, id_1,  name, device_type):
    def create_device():
        item_device = kp.get_items(item_type=item_type, account_id=account_id, item_id=item_id, auth=auth)
        print(item_device)
        data = item_device['data']
        device_type = data.get('device_type')
        owner_id = data.get('owner_id')
        name = data.get('name')

        device = Device(item_id, name, device_type)
        user = session.query(User).get(owner_id)
        device.user = [user]
        session.add(device)

    # def __init__(self, id_1, name, create_date):
    def create_account():
        item_account = kp.get_items(item_type=item_type, account_id=account_id, item_id=item_id, auth=auth)
        print(item_account)
        data = item_account['data']
        account_name = data.get('name')
        account = Account(item_id, account_name, datetime.now())
        session.add(account)

    if item_type == 'user':
        print('inserting users')
        # create_user()
        q = session.query(User.id).filter(User.id == item_id)
        print(q)
        if not session.query(q.exists()).scalar():
            # q = session.query(User).filter(User.id == item_id)
            # session.query(q.)
            create_user()

    if item_type == 'account':
        create_account()

    if item_type == 'device':
        create_device()

    session.commit()
    session.close()







