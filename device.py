from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    extension = Column(Integer)
    device_type = Column(String)
    user_id = Column(Integer, ForeignKey('users3.id'))
    user = relationship("User", backref="devices")

    def __init__(self, extension, device_type, user):
        self.extension = extension
        self.device_type = device_type
        self.user = user
