import reader, book, reviews
from sqlalchemy.ext.declarative import declarative_base
from storage import Database as stor
from book import Book





class Library:


    def __init__(self, storage, name):
        self.storage=storage
        self.name=name
        



    def __repr__(self):
        return f'{self.name},{self.storage}'


    def add_book(self, isbn, author, title, year):
        book=Book(isbn,title,author, int(year))
        return self.storage.add_book(book)



    def del_book(self, book):
        message=self.storage.remove_book(book)
        return message



    def give_book_to_reader(self, book, reader):

        """
        the function change the status lib to status with reader
        status lib means the book is in library
        :param book: book object
        :param reader: reader object
        :return: message with operation
        """
        print('start func')
        if self.storage.status(book)==True:
            self.storage.update_book(book, reader)
            return True
        else:
            return False



    def get_book_from_reader(self,book):
        """
        the func return book from any reader who had it

        """
        if self.storage.status(book)==False:
            self.storage.update_book(book, None)
            return True
        else:
            return False
        
        

    def print_books(self,param, page):
        """the function return books in library depends on parameter

        :param param: could be "all", "in" mean in library, and "out" mean out of library
        :return:
        """
        return self.storage.load_books(param, page)


    """def sort(self,param):
                    if param=="year":
                        sorted_list=sorted(self.list_of_books, key=lambda item:item.year)
                        for i in sorted_list:
                            print(i)
                    elif param=="name":
                        sorted_list = sorted(self.list_of_books, key=lambda item: item.name)
                        for i in sorted_list:
                            print(i)
                    elif param=="author":
                        sorted_list = sorted(self.list_of_books, key=lambda item: item.author)
                        for i in sorted_list:
                            print(i)
                    else:
                        raise Exception("Sorry, keyword wasnt correct")
                    return print("all the books in our library")"""

    def show_user_book(self,user):
        return self.storage.load_readers(user)


    def add_user(self,user1):
        print(f'this is user from library {user1.name}  {user1.password}  {user1.login}  {user1.writer}')
        message=self.storage.add_reader(user1)
        if message==True:
            return f'you registere successfully'
        else:
            return f'something goes wrong, change data and try once more'

    def load_user(self, user_id):
        return self.storage.load_readers(user_id)

    def check_user(self, user):
        a=self.storage.check_reader(user)
        if a:
            return True
        else:
            return False

    def check_login(self, login):
        return self.storage.check_login(login)

    def search_book(self, key):
        return self.storage.search_book(key)


    def find_reviews(self, isbn):
        return self.storage.find_reviews(isbn)


    def get_rate(self, isbn):
        return self.storage.get_rate(isbn)


    def add_review(self,isbn,reader, review, rate):
        add=reviews.Reviews(isbn, reader, review, rate)
        return self.storage.add_review(add)


    def get_reader(self, name):
        return self.storage.get_reader(name)


    def my_books(self,username):
        return self.storage.my_books(username)

