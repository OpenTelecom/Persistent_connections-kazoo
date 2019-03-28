from sqlalchemy import Column, String, Integer, Date

from base import Base
from kazoo_websocket import create_id


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, default=create_id())
    name = Column(String)
    create_date = Column(Date)

    def __init__(self, name, create_date):
        self.create_date = create_date
        self.name = name
