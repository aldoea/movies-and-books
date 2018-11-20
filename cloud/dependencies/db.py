# -​*- coding: utf-8 -*​-import os
import pyodbc 
from json import dumps, loads
from cloud.dependencies import constants as _Constants
from cloud.dependencies import config_db as _Config

driver = _Config.DRIVER
server = _Config.SERVER
database = _Config.DATABASE
trusted = _Constants.TRUSTED

cnxn = pyodbc.connect( 'DRIVER=%s;SERVER=%s;DATABASE=%s;Trusted_Connection=%s;'%(driver, server, database, trusted) ) 
cursor = cnxn.cursor()

def get_data(table, param, primary_key, param2 = None, second_key = None):
	if param2 != None:
		query = "SELECT * FROM {} WHERE {} = '{}' AND {}={}".format(table, param, primary_key, param2, second_key)
	else:		
		query = "SELECT * FROM {} WHERE {} = '{}'".format(table, param, primary_key)
	cursor.execute(query)
	return cursor.fetchone()

def get_table_by_ISBN(subquery):	
	cursor.execute("SELECT * FROM %s" %(subquery))	
	return cursor.fetchone()

def get_table(table):	
	cursor.execute("SELECT * FROM %s" %(table))
	data = []
	while 1:
		row = cursor.fetchone()
		if not row:
			return data		
		data.append(row)
	cnxn.close()

def get_columns_names(table):
	columns = []
	for row in cursor.columns(table='{}'.format(table)):
		columns.append(row.column_name)
	return columns

def search(table, data):
	if table == 'Libro':		
		query = "SELECT * FROM {} WHERE TituloLibro LIKE '%{}%'".format(table, data)
		cursor.execute(query)
		return cursor.fetchall()
	if table == 'Pelicula':
		query = "SELECT * FROM {} WHERE TituloPelicula LIKE '%{}%'".format(table,data)
		cursor.execute(query)
		return cursor.fetchall()

def insert(table, data):
	try:
		if table == 'Libro':
			query = "INSERT INTO {} VALUES ('{isbn}','{title}','{country}',{noEdition},'{originalLanguage}','{adaptedLanguage}','{releaseDate}','{printedDate}',{cveEditorial})".format(table,**data)		
			cursor.execute(query)
			cnxn.commit()
			return True
		if table == 'Pelicula':
			query = "INSERT INTO {} VALUES ('{isbn}','{title}', '{genre}','{release_date}','{runtime}')".format(table,**data)			
			cursor.execute(query)
			cnxn.commit()
			return True
	except Exception as e:
		print 'INSERT FAIL:',e	
		return False
	cnxn.close()

def delete(table, param, primary_key, param2 = None, second_key = None):
	try:
		if param2 != None:			
			query = "DELETE FROM {} WHERE {} = '{}' AND {} = {}".format(table,param,primary_key,param2,second_key)
			print query
		else:
			query = "DELETE FROM {} WHERE {} = '{}'".format(table,param,primary_key)			
		cursor.execute(query)		
		cnxn.commit()
	except Exception as e:
		print 'DELETE FAIL', e				

def update(table, param, primary_key, data, param2 = None, second_key = None):
	try:
		if table == 'Libro':
			query = "UPDATE {} SET ISBN='{isbn}',TituloLibro='{title}',Pais='{country}',NoEdicion={noEdition},IdiomaOriginal='{originalLanguage}',IdiomaAdaptado='{adaptedLanguage}',AnoPublicacion='{releaseDate}',AnoImpresion='{printedDate}',CveEditorial={cveEditorial} WHERE {} = '{}'".format(table, param, primary_key, **data)			
			cursor.execute(query)
			cnxn.commit()
			return True		
		if table == 'Pelicula':
			query = "UPDATE {} SET ISBN='{isbn}', TituloPelicula='{title}', Genero='{genre}', AnoEstreno='{release_date}', Duracion='{runtime}' WHERE {} = '{}' AND {} = {}".format(table, param, primary_key, param2, second_key, **data)
			print query			
			cursor.execute(query)
			cnxn.commit()
			return True		
		return False			
	except Exception as e:
		print 'UPDATE FAIL:',e		
		return False







