# coding=utf-8

# 1 - imports
from datetime import date

from user import User
from base import Session, engine, Base
from device import Device


def insert_item(id, name, date, ):

    # 2 - generate database schema
    Base.metadata.create_all(engine)

# 3 - create a new session
    session = Session()

# 4 - create users
# def __init__(self, name, create_date, no_devices, email):
# bourne_identity = User(1, "user_1", date(2002, 10, 11), email='b@2.com', no_devices=0)
# furious_7 = User(2, "user_2", date(2015, 4, 2), email='b@2.com', no_devices=1)
# pain_and_gain = User(3, "user_3", date(2013, 8, 23), email='b@2.com', no_devices=2)
#
# # 5 - creates devices
# # def __init__(self, extension(INTEGER), device_type(STRING), user):
# matt_damon = Device(1, 5050, "SIP", bourne_identity)
# dwayne_johnson = Device(2, 5051, "SOFT_PHONE", furious_7)
# mark_wahlberg = Device(3, 5052, "SIP", pain_and_gain)
# mark_wahl = Device(4, 5053, "CELL", pain_and_gain)
#
#
# # 9 - persists data
# session.add(bourne_identity)
# session.add(furious_7)
# session.add(pain_and_gain)
#
# session.add(matt_damon)
# session.add(dwayne_johnson)
# session.add(mark_wahlberg)
# session.add(mark_wahl)

    # session.add()


# 10 - commit and close session
    session.commit()
    session.close()
