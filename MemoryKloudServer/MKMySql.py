#!/usr/bin/python
# -*- coding: utf-8 -*-

# MKMySql.py
# jwu April 2, 2012
import MySQLdb, MKconfig, sys, time, os, uuid

#----- INSERT -----
def insertRecord(TableName, NewRecord):
# Insert record into the database
# @parm TableName:		String			the new table name 				(ex. USERS)
# @parm NewRecord:		Dictionary		{column1 name: column1 value, ..}(ex. {'name':'ali', ...}) 
# ~~~~~ WARNING ~~~~~
####	for the new record make sure string values contain a (') cuz the function don't add them
####	ex. "'Ali'" as a name or "\'Ali\'"
# ~~~~~ END ~~~~~~~~~
# @return Boolean
	# building sql statement
	columns = ""
	values = ""
	newId = -1
	for column in NewRecord.keys():
		if len(columns)>1:
			columns += ", "
			values += ", "
		columns += column
		values += str(NewRecord[column])
	sql = "INSERT INTO %s (%s) VALUES (%s)" % (TableName, columns, values)
	# for debugging purpose
	print sql
	# execute the query
	try:
		conn = MySQLdb.connect(host=MKconfig.dbhost,user=MKconfig.dbusername,
                  passwd=MKconfig.dbpasswrd,db=MKconfig.dbcatalog)  
		c = conn.cursor()
		c.execute(sql)
		newId = c.lastrowid
		conn.commit()
		conn.close()
		return newId
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

def insertBLOB(sql, blob):
	newId = -1
	try:
		conn = MySQLdb.connect(host=MKconfig.dbhost,user=MKconfig.dbusername,
                  passwd=MKconfig.dbpasswrd,db=MKconfig.dbcatalog)  
		c = conn.cursor()
		c.execute(sql, (blob) )
		conn.commit()
		newId = c.lastrowid
		conn.close()
		return newId
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return newId

#----- SELECT -----
def SelectRecord(TableName, Fields, Condition):
# Select record from the database
# @parm TableName:		String			the new table name 				(ex. USERS)
# @parm Fields:			List-Strings	a list of fields names (ex.['Name','user_id', ... ])
# @parm Condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# ~~~~~ WARNING ~~~~~
####	for the new record make sure string values contain a (') cuz the function don't add them
####	ex. "'Ali'" as a name or "\'Ali\'"
# ~~~~~ END ~~~~~~~~~
# @return ***
	# building sql statement
	columns, where = "", ""
	for column in Fields:
		if len(columns)>1:
			columns += ", "
		columns += column
	sql = "SELECT %s FROM %s" % (columns, TableName)
	
	if Condition != None:
		for (field, operator, value) in Condition:
			if len(where)>1:
				where += "AND "
			where += "%s%s%s " % (field, operator, value)
		
		sql += " WHERE %s" % (where)
	# for debugging purposes
	print sql
	# run the query
	try:
		conn = MySQLdb.connect(host=MKconfig.dbhost,user=MKconfig.dbusername,
                  passwd=MKconfig.dbpasswrd,db=MKconfig.dbcatalog)
		c = conn.cursor()
		c.execute(sql)
		rows = c.fetchall()
		conn.commit()
		conn.close()
		return rows
	except:
		return []
	return []

# ---- RUN SQL directly
def ExecSqlQuery(sql):
	print sql
	try:
		conn = MySQLdb.connect(host=MKconfig.dbhost,user=MKconfig.dbusername,
                  passwd=MKconfig.dbpasswrd,db=MKconfig.dbcatalog)
		c = conn.cursor()
		c.execute(sql)
		rows = c.fetchall()
		conn.commit()
		conn.close()
		return rows
	except:
		return []
	return []
	
# ---- RUN SQL directly
def ExecSql(sql):
# Execute the given sql
# @parm sql:		String	 The SQL to be executed
	print sql
	try:
		conn = MySQLdb.connect(host=MKconfig.dbhost,user=MKconfig.dbusername,
                  passwd=MKconfig.dbpasswrd,db=MKconfig.dbcatalog)  
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		conn.close()
		return True
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return False
	
# ---- MK DB ------
def GetUniqueID(Record_Type='None'):
	Record_Type = str(Record_Type)
	idtime = str(uuid.uuid1(int(time.time()*100000)))
	if Record_Type == 'USERS':
		return "'u%s'" % (idtime)
	elif Record_Type == 'KLOUDLETS':
		return "'e%s'" % (idtime)
	elif Record_Type == 'MOMENTS':
		return "'n%s'" % (idtime)
	elif Record_Type ==	'FILES':
		return "f%s" % (idtime.replace("-", "f"))
	elif Record_Type ==	'INVITE':
		return "i%s" % (idtime)
	else:
		return "o%s" % (idtime)
		



		

	
		

		
