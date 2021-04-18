from sqlalchemy import create_engine
from base_class_sql import Base
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, select, and_, or_
from book import Book
from reader import Reader
from reviews import Reviews
from sqlalchemy.sql import func

ROWS_PER_PAGE=20



import csv
import os









class Database:
    def __init__ (self,db_type, username, password, adress, port, name):


        self.engine = create_engine(f'{db_type}://{username}:{password}@'
                                    f'{adress}:{port}/{name}')


        # create table
        #Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)





        # create session
        self.session = Session(self.engine)

    def add_book(self, book):
        try:
            self.session.add(book)
            self.session.commit()
        except:
            return False
        return True

    def remove_book(self, book) -> bool:
        self.session.query(Book).filter(Book.isbn==book).delete()
        try:
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True

    def update_book(self, isbn, reader) -> bool:

        """a = self.session.query(Book).filter(Book.isbn == isbn).all()
         if len(a):
            self.session.query(Book).filter(Book.isbn==isbn).update({Book.status:reader}, synchronize_session = False)
            return True"""
        try:

            a=self.session.query(Book).filter(Book.isbn==isbn).all()
            a[0].status=reader
            self.session.commit()
            return True
        except:
            #self.session.rollback()
            return False


    def load_books(self, param, page):
        if param=="all":
            list_book=self.session.query(Book).all()
            if len(list_book)<20:
                return list_book, len(list_book)
            a=self.session.query(Book).limit(20).offset(page*20).all()
            length=len(self.session.query(Book).all())
            return a, length
        elif param=='in':
            return self.session.query(Book).filter(Book.status=="lib").paginate(page=page, per_page=ROWS_PER_PAGE)
        else:
            return self.session.query(Book).filter(Book.status!="lib").paginate(page=page, per_page=ROWS_PER_PAGE)

    def add_reader(self, user) -> bool:
        #self.session.add(user)
        try:
            self.session.add(user)
            self.session.commit()
        except:
            self.session.rollback()
            print(f'this is except {user}')
            return False
        return True




    def load_readers(self, user_id):
        return self.session.query(Reader).filter(Reader.id == user_id).first()






    def check_reader(self, obj_reader: Reader):
        try:
            a = self.session.execute(self.session.query(Reader).filter(and_(Reader.login == obj_reader.login,
                                                                   Reader.password==obj_reader.password))).all()
            print(a)
            if len(a):
                return True
            else:
                return False
        except:
            self.session.rollback()
            return None

    def check_login(self,login):
        try:
            a=self.session.query(Reader).filter(Reader.login==login).all()
            if len(a):
                return True
            else:
                return False
        except:
            self.session.rollback()
            return False

    def search_book(self,key)->list:
        key="%"+key+"%"
        a=self.session.query(Book).filter(or_(Book.author.like(key), Book.title.like(key),Book.isbn.like(key))).all()

        return a

    def find_reviews(self, isbn):
        value=self.session.query(Reviews).filter(Reviews.isbn==isbn).all()
        return value


    def get_rate(self, isbn):
        val=self.session.query(func.avg(Reviews.rate).filter(Reviews.isbn==isbn)).one()
        return val

    def get_reader(self, name):
        a=self.session.query(Reader).filter(Reader.login==name).one()
        return a





    def add_review(self,review):
        self.session.add(review)
        try:
            self.session.commit()
        except:
            return False
        return True


    def status(self,isbn):
        a=self.session.query(Book).filter(Book.isbn==isbn).all()
        if self.session.query(Book).filter(Book.isbn==isbn)[0].status==None:
            return True
        else:
            return False


    def my_books(self, username):
        return self.session.query(Book).filter(Book.status==username).all()



    def import_db(self,file_name):
        f = open(file_name)
        reader = csv.reader(f)
        for isbn, title, author, year in reader:
            if year.isnumeric():
                year=int(year)
            else:
                year=0
            book=Book(isbn=isbn, title=title, author=author, year=year, status=None)
            self.add_book(book)

        return True







