from sqlalchemy import Column, String, Date

from base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True)
    name = Column(String)
    create_date = Column(Date)

    def __init__(self, id_1, name, create_date):
        self.id = id_1
        self.create_date = create_date
        self.name = name
