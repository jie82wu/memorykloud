# MKController.py
# April 7th, 2012 JWU
# Interface between Viewer (MKHTML/MKJOSON) and Data Model (MKMySQL)

import MKMySql, MKconfig
import sys, time, os, uuid

def GetUsers(columns, condition):
# return all the active moments
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return data rows
	# Add condition
	if condition == None:
		condition = [('IS_DELETED', '=', '0')]
	else:
		condition.append(('IS_DELETED', '=', '0'))	
	
	rows = MKMySql.SelectRecord('MK_USERS', columns , condition)
	return rows

def GetKloudlets(columns, condition):
# return all the active kloudlets
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return data rows
	# Add condition
	if condition == None:
		condition = [('IS_DELETED', '=', '0')]
	else:
		condition.append(('IS_DELETED', '=', '0'))	
	
	rows = MKMySql.SelectRecord('MK_KLOUDLET', columns , condition)
	return rows

def GetKloudletsWithCover(columns, condition):
# return all the active kloudlets
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return data rows
	# Add condition
	where = ""
	sql = """	SELECT K.ID, MS.BLOBDATA, K.NAME, K.CREATED_BY, K.DESCRIPTION, K.ACCESS, K.PIN, K.CREATED_ON
				FROM MK_KLOUDLET K 
				LEFT OUTER JOIN MK_KLOUDLET_MOMENT KM
				ON KM.KLOUDLET_ID = K.ID
				INNER JOIN MK_MOMENT M
				ON M.ID = KM.MOMENT_ID
				INNER JOIN MK_MEDIA_STORAGE MS
				ON M.MEDIA_ID = MS.ID
				WHERE K.IS_DELETED=0 AND KM.IS_DEFAULT = true
				ORDER BY K.CREATED_ON """	
	
	rows = MKMySql.ExecSqlQuery(sql);
	return rows

	
def GetMoments(columns, condition):
# return all the active moments
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return data rows
	# Add condition
	if condition == None:
		condition = [('IS_DELETED', '=', '0')]
	else:
		condition.append(('IS_DELETED', '=', '0'))	
	
	where = ""
	sql = "SELECT M.ID, M.TYPE, M.TEXT, M.MEDIA_ID, MS.BLOBDATA, M.URL, M.GEOLOCATION, M.PARENT_ID, M.CREATED_BY, M.CREATED_ON " +	"FROM MK_MOMENT M " +		"LEFT OUTER JOIN MK_MEDIA_STORAGE MS " + "ON M.MEDIA_ID = MS.ID"
	
	if condition != None:
		for (field, operator, value) in condition:
			if len(where)>1:
				where += "AND "
			where += "%s%s%s " % (field, operator, value)
		sql += " WHERE %s" % (where)
	
	
	rows = MKMySql.ExecSqlQuery(sql);
	return rows

def GetMomentsByKloudletId(columns, condition):
# return all the active moments
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return data rows
	# Add condition
	if condition == None:
		condition = [('M.IS_DELETED', '=', '0')]
	else:
		condition.append(('M.IS_DELETED', '=', '0'))	
	
	where = ""
	sql = """	SELECT M.ID, M.TYPE, M.TEXT, M.MEDIA_ID, MS.BLOBDATA, M.URL, M.GEOLOCATION, M.PARENT_ID, U.FULL_NAME, M.CREATED_ON 
				FROM MK_MOMENT M 
				INNER JOIN MK_KLOUDLET_MOMENT KM
				ON KM.MOMENT_ID = M.ID
				INNER JOIN MK_USERS U
				ON U.ID = M.CREATED_BY
				LEFT OUTER JOIN MK_MEDIA_STORAGE MS 
				ON M.MEDIA_ID = MS.ID"""
	
	if condition != None:
		for (field, operator, value) in condition:
			if len(where)>1:
				where += "AND "
			where += "%s%s%s " % (field, operator, value)
		sql += " WHERE %s" % (where)
	
	sql += " ORDER BY M.CREATED_ON"
	
	rows = MKMySql.ExecSqlQuery(sql);
	return rows

	
def GetUserHandle(user_id):
# @parm user_id:		String		The user_id you want to git login for
# @ return html
	rows = MKMySql.SelectRecord('MK_USERS', ['USER_HANDLE'] , [("ID", "=", str(user_id))])
	user_handle = 'N/A'
	for row in rows:
		user_handle = str(row[0])
	return user_handle

def GetTIMESTAMP():
	return str(time.strftime("%Y-%m-%d %H:%M:%S"))
	
def AddNewKloudlet(user_id, kloudlet_name):
# Insert new event record into the databae
# @parm user_id:				String 			Createor user_id (ex. 100921)
# @parm event_name:				String			New event name (ex. MemoryKloud Bithday Party)
	NewRecord = {}
	TIMESTAMP = "'%s'" % (GetTIMESTAMP())
	MKconfig.STATUS['kloudlets']  += 1
	NewRecord['NAME'] = "'%s'" % (kloudlet_name)
	NewRecord['CREATED_BY'] = "'%s'" % (user_id)
	NewRecord['CREATED_ON'] = TIMESTAMP
	NewRecord['LAST_UPDATED_BY'] = "'%s'" % (user_id)
	NewRecord['LAST_UPDATED_ON'] = TIMESTAMP
	return MKMySql.insertRecord('MK_KLOUDLET', NewRecord)
	
def AddNewUser(user_fullname, user_email, user_handle ='N/A'):
# Insert new user record into the database
# @parm user_fullname			String 			User full name 
# @parm user_email			String 			User email 
# @parm user_handle				String 			User Handle 
# @return INT 			(-1 if fail, user_id if success)
	NewRecord = {}
	TIMESTAMP = "'%s'" % (GetTIMESTAMP())
	MKconfig.STATUS['users'] +=1
	NewRecord['FULL_NAME'] = "'%s'" % (user_fullname)
	NewRecord['EMAIL'] = "'%s'" % (user_email)
	NewRecord['USER_HANDLE'] = "'%s'" % (user_handle)
	NewRecord['JOINED'] = TIMESTAMP
	return MKMySql.insertRecord('MK_USERS', NewRecord)

def AddNewMoment(user_id, kloudlet_id, moment_text):
# Insert new note record into the database
# @parm user_id:				int 			User id number
# @parm kloudlet_id:				int 			KLOUDLET id number
# @parm moment_text				String			moment_text
# @return INT 			(-1 if fail, note_id if success)
	NewRecord = {}
	MKconfig.STATUS['moments'] += 1
	NewRecord['TEXT'] = "'" + moment_text + "'"
	NewRecord['CREATED_BY'] = "'%s'" % (user_id)
	NewRecord['CREATED_ON'] =  "'%s'" % (GetTIMESTAMP())
	
	#TODO: THIS IS SUPPOSED TO BE A TRANSACTION, we don't have transaction support currently
	moment_id = MKMySql.insertRecord('MK_MOMENT', NewRecord)
	sql = "INSERT INTO MK_KLOUDLET_MOMENT (kloudlet_id, moment_id) VALUES ('%s','%s')" % (kloudlet_id, moment_id)
	MKMySql.ExecSql(sql)
	return moment_id

def AddNewFile(user_id, kloudlet_id, description, file_body, file_name):
# Insert new note record into the database
# @parm user_id:				int 			User id number
# @parm kloudlet_id:				int 			KLOUDLET id number
# @parm description:				string 			moment description
# @parm file_body				BLOB			File body
# @parm file_name				String 			File name with an extenetion (ex photo1.jpg)
# @return INT 			(-1 if fail, note_id if success)
	MKconfig.STATUS['files'] +=1
	
	#TODO: THIS IS SUPPOSED TO BE A TRANSACTION, we don't have transaction support currently
	sql = "INSERT INTO MK_MEDIA_STORAGE (TYPE, NAME, BLOBDATA) VALUES (1,'" + file_name + "', %s)" 
	media_id = MKMySql.insertBLOB(sql, file_body)
	
	NewRecord = {}
	NewRecord['TYPE'] = 1 
	NewRecord['MEDIA_ID'] = media_id 
	NewRecord['TEXT'] = "'%s'" % (description)
	NewRecord['CREATED_BY'] = "'%s'" % (user_id)
	NewRecord['CREATED_ON'] =  "'%s'" % (GetTIMESTAMP())
	moment_id = MKMySql.insertRecord('MK_MOMENT', NewRecord)
	
	sql = "INSERT INTO MK_KLOUDLET_MOMENT (kloudlet_id, moment_id) VALUES (%s,%s)" % (kloudlet_id, moment_id)
	MKMySql.ExecSql(sql)
	
	return media_id
	
def IsUserKloudletCreator(user_id, kloudlet_id):
	kloudlets = MKMySql.SelectRecord('MK_KLOUDLET', ['ID'], [('CREATED_BY', '=', user_id ),('ID', '=', kloudlet_id)])
	if len(kloudlets) >= 1:
		return True
	else:
		return False
		
def AddNewInvitaion(inviter_id, kloudlet_id, guest_name,guest_email):
	new_user_id = None
	users = MKMySql.SelectRecord('MK_USERS', ['ID'], [('EMAIL', '=', "\'" + str(guest_email)+ "\'")])
	
	if IsUserKloudletCreator(inviter_id, kloudlet_id):
		if len(users) == 0: # if the user doesn't exist in db
			new_user_id = AddNewUser(guest_name, guest_email, guest_email)
			if new_user_id == -1:
				return 406 # can not create user
		else:
			new_user_id = users[0][0]
		NewRecord = {}
		NewRecord['CREATED_BY'] = new_user_id
		NewRecord['CREATED_ON'] =  "'%s'" % (GetTIMESTAMP())
		NewRecord['MESSAGE'] = "'You are invited by %s'" % (GetUserHandle(inviter_id))
		
		#TODO: THIS IS SUPPOSED TO BE A TRANSACTION, we don't have transaction support currently
		invite_id = -1
		invite_id = MKMySql.insertRecord('MK_INVITES', NewRecord)
		if (invite_id >= 0):
			# MKemails.mailid(guest_email,invite_id, MKHTML.GetKloudletName(kloudlet_id))
			sql = "INSERT INTO MK_INVITES_MEMBERS (invite_id, user_id, kloudlet_id) VALUES (%s, %s, %s)" % (invite_id, new_user_id, kloudlet_id)
			MKMySql.ExecSql(sql)
		return invite_id
	else:
		return 401 # no permission
		
