# -​*- coding: utf-8 -*​-import os
from flask import render_template, redirect, url_for
from json import dumps
from cloud.dependencies import db as _DB
from cloud.dependencies import constants as _Constants

table = 'Libro'
param = 'ISBN'

def book_handler(request, isbn):
	if request.method == 'DELETE':	
		return delete_book(isbn)
	if request.method == 'POST':		
		book_data = book_data_dicc(request.values)
		if(_DB.update(table, param, isbn, book_data)):
			return redirect(url_for('books'))
		else:
			return render_template('editBook.html', book_data = get_book_data(isbn))
	return render_template('editBook.html', book_data = get_book_data(isbn))

def get_books():
	data = _DB.get_table(table)	
	return render_template('books.html', data = data)

def get_book_data(isbn):
	book_data = _DB.get_data(table, param, isbn)		
	return book_data

def book_details(request, isbn):
	subquery_author = "Autor a where a.CveAutor in (select ep.CveAutor from EscritoPor ep where ep.ISBN = '{}')".format(isbn)
	subquery_editorial = "Editorial e where e.CveEditorial in ( select CveEditorial from Libro where ISBN = '{}')".format(isbn)
	subquery_characters = "Personaje p where p.ISBN = '{}'".format(isbn)
	characters_data = _DB.get_table(subquery_characters)
	author_data = _DB.get_table_by_ISBN(subquery_author)
	editorial_data = _DB.get_table_by_ISBN(subquery_editorial)
	book_data = get_book_data(isbn)	
	return render_template("bookDetail.html", book_data = book_data, author_data = author_data, characters_data = characters_data, editorial_data = editorial_data)	


def book_data_dicc(data):
	book_data = {}
	book_data['isbn'] = data['ISBN']
	book_data['title'] = data['title']
	book_data['country'] = data['country']
	book_data['noEdition'] = data['numEdition']
	book_data['originalLanguage'] = data['originalLanguage']
	book_data['adaptedLanguage'] = data['adaptedLanguage']
	book_data['releaseDate'] = data['releaseDate']
	book_data['printedDate'] = data['printedDate']
	book_data['cveEditorial'] = data['cveEditorial']
	return book_data

def create_book(request):
	if request.method == 'POST':		
		book_data = book_data_dicc(request.values)
		if( _DB.insert(table, book_data) ):			
			return redirect(url_for('books'))
		else:			
			return render_template('createBook.html')
	else:
		#return redirect(url_for('create_movie'))
		return render_template('createBook.html')


def delete_book(isbn):	
	_DB.delete(table, param ,isbn)
	return redirect(url_for('books'))	

#def update_book():	
#	_DB.delete(table, param ,isbn, book_data)
#	return render_template('books.html')		