from sqlalchemy import Column, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from base import Base


class Call(Base):
    __tablename__ = 'calls'

    calls_users_association = Table(
        'calls_users', Base.metadata,
        Column('call_id', String, ForeignKey('calls.id')),
        Column('user_id', String, ForeignKey('users.id'))
    )

    id = Column(String, primary_key=True)
    create_date = Column(Date)
    to = Column(String)
    from_m = Column(String)
    duration = Column(String)
    user = relationship("User", secondary=calls_users_association)

    def __init__(self, id_i, create_date, to, from_m, duration):
        self.id = id_i
        self.create_date = create_date
        self.to = to
        self.from_m = from_m
        self.duration = duration
