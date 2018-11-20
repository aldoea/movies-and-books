# -​*- coding: utf-8 -*​-import os
from flask import render_template, redirect, url_for
from json import dumps
from cloud.dependencies import db as _DB
from cloud.dependencies import constants as _Constants

def search(request):
	search_string = request.values['search']
	table = request.values['table']	
	print table
	results = _DB.search(table, search_string)
	if table == 'Libro':
		return render_template('books.html', data = results)		
	if table == 'Pelicula':
		return render_template('movies.html', data = results)