from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, ForeignKey, select
from base_class_sql import Base


class Reviews(Base):
    __tablename__= "reviews"
    def __init__(self, isbn, reader, review, rate):
        self.isbn=isbn
        self.reader = reader
        self.review=review
        self.rate=rate




    id = Column(Integer, primary_key=True)
    isbn=Column(Text, ForeignKey('book.isbn'))
    reader = Column(Text)
    review = Column(Text)
    rate=Column(Integer)

    def __repr__(self):
        return f'{self.isbn}, {self.reader}, {self.review}'