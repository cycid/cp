import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import Library,reader
from storage import Database
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename








app=Flask(__name__)
app.secret_key = '56fgpknn5kp'
app.config['UPLOAD_FOLDER']='./storage'
app.config['MAX_CONTENT_PATH']=3000000
app.config['LOGIN_DISABLED']=False
app.config['TESTING']=False
login_manager=LoginManager(app)
login_manager.login_view='one'






#main page
KEY="LMkmCT1hycZRWqvDAZnmJA"
@app.route("/")
def one():
	if current_user.is_authenticated:
		return redirect (url_for('search'))
	flash("please login")
	return render_template ("index.html");

@app.route("/registration")
def registration():
	if current_user.is_authenticated:
		return redirect(url_for("search"))

	return render_template ("registration.html");


#registration function
@app.route("/engines", methods=["POST"])
def engines():
	user_login=request.form.get("username")
	password=request.form.get("pass")
	name=request.form.get("name")
	writer=request.form.get("writer")
	user=reader.Reader(user_login,password,name, writer)

	if my_lib.check_login(user.login)==True:
		flash("username already exist")
		return render_template("registration.html")
	my_lib.add_user(user)
	flash("thank you for registering")
	return  render_template("index.html")


#login function
@app.route("/login", methods=["POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('search'))
	user=reader.Reader(request.form.get("usernamelog"), request.form.get("passlog"), "any", "any")
	if my_lib.check_user(user)==True:
		print('this way')
		reader1=my_lib.get_reader(request.form.get("usernamelog"))
		login_user(reader1)
		#session['user']=request.form.get("usernamelog")
		return redirect (url_for("search"))
	else:
		flash("incorrect username or password")
		return render_template("index.html")


#search function and page

@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
	book_list=my_lib.search_book(current_user.writer)
	return render_template('search.html', nn='reader', recomended=book_list[0:5])



#drop sesion and redirect to main page
@app.route("/logout")
def logout():
	logout_user()
	#session.pop('user', None)
	return redirect (url_for("one"))


#Searchresult page
@app.route("/result", methods=["POST"])
@login_required
def result():
	result=my_lib.search_book(request.form.get("wordrequest"))
	if len(result)==0:
		flash("there is no such result")
		return render_template("index.html")
	return render_template("result.html", booksres=result)


#book page
@app.route("/book/<isbn>")
@login_required
def book(isbn):
	book_example=my_lib.search_book(isbn)
	if len(book_example)!=1:
		flash('please enter correct isbn')
		return render_template('search.html')
	if book_example[0].status==current_user.login:
		status=True
	elif book_example[0].status==None:
		status=False
	else:
		status=None
	reviews=my_lib.find_reviews(isbn)
	avg_rate=my_lib.get_rate(isbn)
	if avg_rate[0]==None:
		avg_rate='no rate yet'
	else:
		avg_rate=round(avg_rate[0],2)
	print(status)
	return render_template("book.html", bookbook=book_example[0], reviews=reviews, rate=avg_rate, isbn=isbn, status=status)


#write review function
@app.route("/review/<isbn>")
@login_required
def review(isbn):
	comment=request.args.get("review")
	rate=request.args.get("rate", type=int)
	user=current_user.name
	if my_lib.add_review(isbn, user, comment, rate)==True:
		flash("thank you for comment")
		return redirect(url_for("book", isbn=isbn))
	else:
		flash("Error, try once more")
		return redirect(url_for("book", isbn=isbn))



#api function
@app.route("/api/<isbn>")
def api(isbn):
	bookss=my_lib.search_book(isbn)[0]
	print(bookss)
	if bookss is None:
		return jsonify({"error":"isbn doesnt exist in our database"}), 404
	review_count=len(my_lib.find_reviews(isbn))
	score=float(my_lib.get_rate(isbn)[0])
	return jsonify({
		"title": bookss.title,
		"author": bookss.author,
		"year": bookss.year,
		"isbn": isbn,
		"review_count": review_count,
		"average_score": score
		})

@app.route("/takebook/<isbn>")
@login_required
def takebook(isbn):
	username = current_user.login
	result = my_lib.give_book_to_reader(isbn, username)
	if result==True:
		flash('you get the book')
		return redirect(url_for("book", isbn=isbn))
	else:
		flash('somthing goes wrong')
		return redirect(url_for("book", isbn=isbn))


@app.route("/give_book/<isbn>", methods=["POST"])
@login_required
def give_book(isbn):
	username = current_user.name
	result = my_lib.get_book_from_reader(isbn)
	if result==True:
		flash('book was returned to library')
		return redirect(url_for("book", isbn=isbn))
	else:
		flash('somthing goes wrong')
		return redirect(url_for("book", isbn=isbn))

@app.route("/my_books")
@login_required
def my_books():
	if current_user.is_authenticated:
		book_list=my_lib.my_books(current_user.login)
		if len(book_list):
			return render_template("my_books.html", book_list=book_list)
		else:
			flash("you have no books")
			return redirect(url_for("search"))
	return redirect(url_for('one'))


@app.route('/return_books', methods=["POST"])
@login_required
def return_books():
	books_to_return=request.form.getlist('check')
	for book in books_to_return:
		my_lib.get_book_from_reader(book)
	flash('books were returned')
	return redirect(url_for("search"))


@app.route("/show_all_books")
@login_required
def show_all_books():
	page = request.args.get('page', 1, type=int)
	books, length=my_lib.print_books("all", page)
	length=(length//20)+2
	return render_template("show_all_books.html", book_list=books, length=length, page=page)



@app.route("/delete_books", methods=["POST", "GET"])
@login_required
def delete_books():
	if request.method=="POST":
		del_books=request.form.getlist('check')
		isbn=[]
		for book in del_books:
			a=my_lib.del_book(book)
			if a==False:
				isbn.append(book)
		if len(isbn):
			flash(f'books with {isbn} were not deleted')
		else:
			flash('books were deleted')
			return redirect(url_for("delete_books"))
	else:
		page = request.args.get('page', 1, type=int)
		books, length = my_lib.print_books("all", page)
		length = (length // 20) + 2
		return render_template("books_to_delete.html", book_list=books, length=length, page=page)



@app.route('/add_book', methods=["POST", "GET"])
@login_required
def add_book():
	if request.method=='POST':
		a=my_lib.add_book(request.form.get('isbn'),request.form.get('author'), request.form.get('title'), request.form.get('year'))
		if a==True:
			flash('book was added successfully')
			return redirect(url_for('add_book'))
		else:
			flash('data wasnt correct try once more')
			return redirect(url_for('add_book'))

	else:
		return render_template('sava_book.html')


@login_manager.user_loader
def user_loader(user_id):
	return my_lib.load_user(user_id)


@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		if f:
			filename=secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			if my_lib.storage.import_db(f'./storage/{f.filename}')==True:
				flash('books was added')
				return redirect(url_for("add_book"))
			flash("error, some books wasnt added")
			return redirect(url_for("add_book"))
		flash("error, file wasnt uploaded")
		return redirect(url_for("add_book"))
	return render_template("upload.html")




if __name__ == '__main__':
	a = Database("postgresql", "postgres", "12345", "localhost", '5432', 'library')
	my_lib=Library.Library(a,"my_lib")

	app.run(debug=True)



