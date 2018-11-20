from flask import render_template, redirect, url_for
from cloud.dependencies import db as _DB
from cloud.dependencies import constants as _Constants

table = 'Pelicula'
param = 'ISBN'
param2 = 'CvePelicula'

def movie_handler(request, isbn, cve_movie):
	if request.method == 'DELETE':	
		return delete_movie(isbn, cve_movie)
	if request.method == 'POST':	
		movie_data = movie_data_dicc(request.values)
		if(_DB.update(table, param, isbn, movie_data, param2, cve_movie)):
			print "------IF update enter"
			return redirect(url_for('movies'))
		else:
			print "-----ELSE ENTER"			
			return render_template('editMovie.html', movie_data = get_movie_data(isbn, cve_movie))
	print get_movie_data(isbn, cve_movie)			
	return render_template('editMovie.html', movie_data = get_movie_data(isbn, cve_movie))

def get_movies():
	data = _DB.get_table(table)	
	return render_template('movies.html', data = data)

def get_movie_data(isbn, cve_movie):
	movie_data = _DB.get_data(table, param, isbn, param2, cve_movie)		
	return movie_data

def movie_details(isbn, cve_movie):	
	subquery_director = "Director d where d.CveDirector in (select dp.CveDirector from DirigidaPor dp where dp.ISBN = '{}' and dp.CvePelicula = {})".format(isbn, cve_movie)
	subquery_productor = "Productor	where CveProductor in ( select CveProductor from ProducidaPor where ISBN = '{}' and CvePelicula = {})".format(isbn, cve_movie)
	subquery_actor = "Actor where CveActor in ( select CveActor from ActuadaPor where ISBN = '{}' and CvePelicula = {})".format(isbn, cve_movie)
	director_data = _DB.get_table(subquery_director)
	productor_data = _DB.get_table(subquery_productor)
	actor_data = _DB.get_table(subquery_actor)
	movie_data = get_movie_data(isbn, cve_movie)		
	return render_template("movieDetail.html", director_data = director_data, actor_data = actor_data, movie_data = movie_data, productor_data = productor_data)	


def movie_data_dicc(data):	
	movie_data = {}	
	movie_data['isbn'] = data['ISBN']	
	movie_data['title'] = data['title']	
	movie_data['genre'] = data['genre']	
	movie_data['release_date'] = data['release_date']		
	movie_data['runtime'] = data['runtime']		
	return movie_data

def create_movie(request):	
	if request.method == 'POST':				
		movie_data = movie_data_dicc(request.values)				
		if( _DB.insert(table, movie_data) ):			
			return redirect(url_for('movies'))
		else:			
			return render_template('createmovie.html')
	else:
		#return redirect(url_for('create_movie'))
		return render_template('createmovie.html')


def delete_movie(isbn, cve_movie):	
	_DB.delete(table, param ,isbn, param2, cve_movie)
	return redirect(url_for('movies'))	