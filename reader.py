
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, ForeignKey, select
from base_class_sql import Base
from flask_login import UserMixin


class Reader(Base, UserMixin):
    __tablename__= "readers"
    def __init__(self, login, password, name, writer):
        self.login=login
        self.name = name
        self.password=password
        self.writer=writer



    id = Column(Integer, primary_key=True)
    login=Column(Text, unique=True)
    name = Column(Text)
    password = Column(Text)
    writer = Column(Text)

    def __repr__(self):
        return f'{self.name}'