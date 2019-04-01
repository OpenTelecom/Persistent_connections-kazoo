from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Call(Base):
    __tablename__ = 'calls'

    id = Column(Integer, primary_key=True, default=create_id())
    create_date = Column(Date)
    to = Column(String)
    form_m = Column(String)
    duration = Column(Integer)
    user_id = Column(Integer, ForeignKey('users3.id'))
    user = relationship("User", backref="devices")

    def __init__(self, create_date, to, from_m, duration):
        self.create_date = create_date
        self.to = to
        self.from_m = from_m
        self.duration = duration
