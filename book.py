from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, ForeignKey, select
from sqlalchemy.orm import mapper, relationship, Session
from reader import Reader
from base_class_sql import Base
class Book(Base):
    __tablename__= "book"    
    def __init__(self,isbn, title, author, year:int, status=None):
        self.isbn=isbn        
        self.title=title
        self.author=author
        self.year=year
        self.status=status

    id = Column(Integer, primary_key=True)
    isbn=Column(Text, unique=True )
    title = Column(Text)
    author = Column(Text)
    year = Column(Integer)

    status = Column(Text, ForeignKey('readers.login'))
    reader = relationship('Reader', backref='books')






    def __repr__(self):
        return f'{self.title} by {self.author} published in {self.year} in {self.status}'








