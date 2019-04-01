from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship


from base import Base


class Device(Base):
    __tablename__ = 'devices'

    devices_users_association = Table(
        'devices_users', Base.metadata,
        Column('device_id', String, ForeignKey('devices.id')),
        Column('user_id', String, ForeignKey('users.id'))
    )

    id = Column(String, primary_key=True)
    device_type = Column(String)
    name = Column(String)
    user = relationship("User", secondary=devices_users_association)

    def __init__(self, id_1,  name, device_type):
        self.id = id_1
        self.name = name
        self.device_type = device_type
