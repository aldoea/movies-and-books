# -​*- coding: utf-8 -*​-
#from json import dumps
#from cloud.app import session as _Session
#from cloud.app import sync as _Sync
#from flask import render_template # url_for , request, redirect, session, escape
import os
from flask import Flask
from flask import render_template, request, url_for
from cloud.app.controllers import movie_controller as _MC
from cloud.app.controllers import book_controller as _BC
from cloud.app.controllers import search_controller as _SC
from cloud.dependencies import constants as _Constants

app = Flask(__name__)
app.secret_key = os.urandom(24)

# G E N E R A L

@app.route("/")
def index():	
	return render_template('index.html')

@app.route("/search" ,methods=["GET"])
def search():
	return _SC.search(request)

# B O O K S	

@app.route("/books")
def books():
	return _BC.get_books()

@app.route("/books/create", methods=['GET', 'POST'])
def create_book():
	return _BC.create_book(request)	

@app.route("/books/<isbn>", methods=['GET','DELETE', 'POST'])
def book_handler(isbn):	
	return _BC.book_handler(request, isbn)

@app.route("/books/<isbn>/details", methods=['GET'])
def book_details(isbn):	
	return _BC.book_details(request, isbn)

# M O V I E S	

@app.route("/movies")
def movies():	
	return _MC.get_movies()

@app.route("/movies/create", methods=['GET', 'POST'])
def create_movie():
	return _MC.create_movie(request)	

@app.route("/movies/<isbn>/<cve_movie>", methods=['GET','DELETE', 'POST'])
def movie_handler(isbn, cve_movie):	
	return _MC.movie_handler(request, isbn, cve_movie)

@app.route("/movies/<isbn>/<cve_movie>/details", methods=['GET'])
def movie_details(isbn, cve_movie):	
	return _MC.movie_details(isbn, cve_movie)


if __name__ == "__main__":
	app.debug = _Constants.DEBUG_MODE
	app.run()	
	url_for('static', filename='bootstrap.css')
	url_for('static', filename='bootstrap.min.css')
	url_for('static', filename='bootstrap.min.js')
	url_for('static', filename='bootstrap.js')
	url_for('static', filename='jquery.js')