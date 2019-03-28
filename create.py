
from user import User
from device import Device
from account import Account
from call import Call


# def __init__(self, id_1, name, create_date, no_devices, email):
def create_user(name, date_created, no_devices, email):
    # user_id = create_id()
    user = User(name, date_created, no_devices, email)
    return user


# def __init__(self,id_1, extension, device_type, user):
def create_device(extension, device_type, user):
    device = Device(extension, device_type, user)
    return device


# def __init__(self, name, create_date):
def create_account(name, date_created):
    account = Account(name, date_created)
    return account


# def __init__(self, create_date, to, from_m, duration):
def create_call(date_created, to, duration, user):
    call = Call(date_created, to, duration, user)
    return call


