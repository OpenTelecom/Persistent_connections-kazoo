from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config


params = config()
host = params.get('host')
user = params.get('user')
password = params.get('password')
database = params.get('database')


engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


