
from base import Session, engine, Base
import kazoo_put as kp
from user import User
from device import Device
from account import Account
from datetime import datetime
from call import Call


def insert_data(item_type, account_id, item_id, auth, **users):

    Base.metadata.create_all(engine)
    session = Session()

    # def __init__(self, id_id, name, create_date, no_devices, email, account):
    def create_user():
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

    # def __init__(self, id_i, create_date, to, from_m, duration):
    def create_call():
        print('inserting calls')
        outbound = users.get('outbound')
        print(outbound)
        inbound = users.get('inbound')
        print(inbound)
        to_name = users.get('callee')
        from_name = users.get('caller')
        duration = users.get('duration')
        if outbound is not None:
            p = session.query(Call.id).filter(Call.id == item_id)
            if not session.query(p.exists()).scalar():
                print(type(p))
                print(p)
                print('in outbound original')
                to = session.query(User).get(users.get('outbound'))
                call = Call(item_id, datetime.now(), to_name, from_name, duration)
                print('main, inbound-CallObject', call)
                print('in outbound', outbound)
                print('in outbound', inbound)
                print(call.user)
                call.user = [to]
                print(call.user)
                session.add('outbound', call)
            else:
                print('in else outbound')
                to = session.query(User).get(users.get('outbound'))
                call = session.query(Call).get(item_id)
                print('else, inbound-CallObject', call)
                print('else, outbound', call.user)
                call.user.append(to)
                print('else, outbound', call.user)

        elif inbound is not None:
            p = session.query(Call.id).filter(Call.id == item_id)
            if not session.query(p.exists()).scalar():
                print('in inbound original')
                from_u = session.query(User).get(users.get('inbound'))
                print(outbound)
                print(inbound)
                call = Call(item_id, datetime.now(), to_name, from_name, duration)
                print('main, outbound-CallObject', call)
                call.user = [from_u]
                print('')
                print('main, inbound', call.user)
                session.add(call)
            else:
                print('in else inbound')
                from_u = session.query(User).get(users.get('inbound'))
                call = session.query(Call).get(item_id)
                print('inbound-else-callObject', call)
                print('else inbound', call.user)
                call.user.append(from_u)
                print(call.user)

        # print(outbound, inbound, to_name, from_name, duration)

    if item_type == 'user':
        print('inserting users')
        q = session.query(User.id).filter(User.id == item_id)
        print(q)
        if not session.query(q.exists()).scalar():
            create_user()

    if item_type == 'account':
        create_account()

    if item_type == 'device':
        create_device()
    if item_type == 'call':
        create_call()

    session.commit()
    session.close()
