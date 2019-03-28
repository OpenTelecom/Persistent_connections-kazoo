from sqlalchemy import Column, String, Integer, Date

from base import Base


class User(Base):
    __tablename__ = 'users4'

    id = Column(String, primary_key=True)
    name = Column(String)
    create_date = Column(Date)
    no_devices = Column(Integer)
    email = Column(String)

    def __init__(self, id_id, name, create_date, no_devices, email):
        self.id = id_id
        self.name = name
        self.create_date = create_date
        self.no_devices = no_devices
        self.email = email
