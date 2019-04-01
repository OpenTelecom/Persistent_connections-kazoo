from sqlalchemy import Column, String, Integer, Date, ForeignKey

from base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    create_date = Column(Date)
    no_devices = Column(Integer)
    email = Column(String)
    account_id = Column(String, ForeignKey('accounts.id'))
    account = relationship("Account", backref="accounts")

    def __init__(self, id_id, name, create_date, no_devices, email, account):
        self.id = id_id
        self.name = name
        self.create_date = create_date
        self.no_devices = no_devices
        self.email = email
        self.account = account
