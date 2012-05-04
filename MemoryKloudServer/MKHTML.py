import MKconfig, MKMySql, MKController, MKUtils

def HomeIndex():
	html = """
	MemoryKloud Home<br>
	<hr>
	<a href='/admin'>	Admin View		</a><br>
	<a href='/user'>	Create User		</a><br>
	<a href='/kloudlet'>	Create Kloudlet	</a><br>
	<a href='/moment'>	Add Moment		</a><br>
	<a href='/file'>	Add File		</a><br>
	<a href='/invite'>	Invite			</a><br>
	<hr>
	""" 
	return html
	
def AdminIndex():
	print MKconfig.STATUS
	HTML_status = '<pre>'
	HTML_status += "REST:" + str(MKconfig.STATUS['REST']) 
	HTML_status += "\n----- counters -----\n"
	HTML_status += "<a href='/kloudlet?id=all'>kloudlets</a>\t"
	HTML_status += "<a href='/user?id=all'>users</a>\t"
	HTML_status += "moments\t"		
	HTML_status += "files\t\n"
	for ctype in ['kloudlets','users','moments','files']:
		HTML_status += str(MKconfig.STATUS[ctype]) + "\t"
	HTML_status += "\n"
	HTML_status += "\n----- Requests -----\n"
	for URI in ['/','/admin', '/kloudlet', '/user', '/moment']:
		HTML_status +=  URI + "\n"
		HTML_status += "\t<font color='#00f'>GET\tPOST\tPUT\tDELETE</font>\n\t"
		
		for HTTP_TYPE in ['GET', 'POST', 'PUT', 'DELETE']:
			HTML_status += str(MKconfig.STATUS[URI][HTTP_TYPE]) + "\t"
		HTML_status += "\n"
	HTML_status += "\n----- ERRORS -----\n"
	for Error in ['ERROR 404', 'ERROR 500']:
		HTML_status +=  "<font color='#f00'>" +Error + "</font>\n"
		HTML_status += "\t<font color='#00f'>GET\tPOST\tPUT\tDELETE</font>\n\t"
		for HTTP_TYPE in ['GET', 'POST', 'PUT', 'DELETE']:
			HTML_status += str(MKconfig.STATUS[URI][HTTP_TYPE]) +"\t"
		HTML_status += '\n'	
	return HTML_status +'</pre>'
	
def NewUserForm():
	html = """
	<form action='/user' method='post'>
	Full name <input type='text' name='fullname'><br>
	Email <input type='text'  name='email'><br>
	<input type='submit'><input type='reset'>
	"""
	return html

def NewKloudletForm():
	html ="""
	<form action='/kloudlet' method='post'>
	User : <select name='UID'>"""
	html +=getOptions('MK_USERS', 'ID', 'FULL_NAME')
	html += """</select><br>
	Kloudlet Name: <input type='text' name='name'><br>
	<input type='submit'><input type='reset'>
	"""
	return html
	
def NewMomentForm():
	html = """
	<form action='/moment' method='post'>
	
	Kloudlet : <select name='EID'>"""
	html += getOptions('MK_KLOUDLET', 'ID', 'NAME')
	html += """</select><br>
	
	User : <select name='UID'>"""
	html += getOptions('MK_USERS', 'ID', 'FULL_NAME')
	html += """</select><br>	
	
	Thought:<input type='text' name='moment' size='140'><br>
	<input type='submit'><input type='reset'>
	"""
	return html

def NewFileForm():
	html= """
	<form enctype="multipart/form-data" action='/file' method='post'>
	
	Event : <select name='kid'>"""
	html +=getOptions('MK_KLOUDLET', 'ID', 'NAME')
	html += """</select><br>
	
	User : <select name='uid'>"""
	html += getOptions('MK_USERS', 'ID', 'FULL_NAME')
	html += """</select><br>	

	Description:<input type='text' name='descp'><br>
	
	File:<input type='file' name='file'><br>
	<input type='submit' value='upload'><input type='reset' value='clear'>
	"""
	return html
	
def NewInviteForm():
	html = """
	<form action='/invite' method='post' id='invite_form'>

	Kloudlet : <select name='EID'>"""
	html += getOptions('MK_KLOUDLET', 'ID', 'NAME')
	html += """</select><br>

	invite from: <select name='UID'>"""
	html += getOptions('MK_USERS', 'ID', 'FULL_NAME')
	html += """</select><br>	"""

	html +="""
	Invite Name:<input type='text' name='new_name'>
	Invite Email: <input type='text' name='new_email'><br>
	<input type='submit'><input type='reset'>
	"""
	return html
	
def getOptions(TABLE_NAME, FIELDVALUE, FIELDNAME):
	html = ''
	rows = MKMySql.SelectRecord(TABLE_NAME, [FIELDVALUE, FIELDNAME] , None)
	flist = []
	for row in rows:
		if row not in flist:
			flist.append(row)
	for values in flist:
		  html += "<option value='%s'>%s</option>" % values
	return html

def ListKloudlets(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return html
	# get the required fields
	RQfields = ['ID', 'NAME', 'CREATED_BY', 'DESCRIPTION','ACCESS', 'PIN', 'CREATED_ON']
	rows = MKController.GetKloudlets(RQfields, condition)
	
	# yield the HTML 
	html ="<table border='1'><tr>"
	for f in RQfields:
		html += "<td>" + f + "</td>"
	html += "</tr>"
	for row in rows:
		html += "<tr>"
		for i,field in enumerate(row):
			if i == 1: # NAME
				html += "<td><a href='/moment?kid=%s'> %s</a></td>" % (row[0],str(field))
			elif i == 2: # CREATED_BY
				html += "<td>" + MKController.GetUserHandle(field) + "</td>"
			else:
				html += "<td>" + str(field) + "</td>"
		html += "</tr>"
	html += "</table>"
	return html

def ListUsers(condition):
# @parm condition:		List-Sets		[(Fiels, operator, value),...] (ex. ('Name', '==', 'Ali'))
# @ return html
	RQfields = ['ID','EMAIL','USER_HANDLE', 'FULL_NAME', 'JOINED']
	rows = MKController.GetUsers(RQfields, condition)
	
	# yield the HTML
	usr = 0
	html ="<table border='1'><tr>"
	for f in RQfields:
		html += "<td>" + f + "</td>"
	html += "</tr>"
	for row in rows:
		html += "<tr>"
		for i,field in enumerate(row):
			if i ==	0: #id
				usr = field
			if i == 1: # email
				html += "<td><a href='/user?id=%s'> %s</a></td>" % (row[0],str(field))
			else:
				html += "<td>" + str(field) + "</td>"
		html += "</tr>"
	html += "</table>"
	return html

def ListMoments(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return html
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMoments(RQfields, condition)
	
	# yield the HTML 
	html ="<table border='1'><tr>"
	for f in RQfields:
		html += "<td>" + f + "</td>"
	html += "</tr>"
	for row in rows:
		html += "<tr>"
		for i,field in enumerate(row):
			if i == 1: # NAME
				html += "<td><a href='/moment?id=%s'> %s</a></td>" % (row[0],str(field))
			elif i == 4: #BLOBDATA
				filePath = ""
				if row[i] != None:
					filePath = MKUtils.GetSubFolder() + "momentId_" + str(row[0]) + ".jpg"
					# TODO: How to render images instead of strings in the browser?
					with open(filePath, "wb") as output_file:
						output_file.write(row[i])
					html += "<td><img src ='file?url=" + filePath + "'></td>"
				else:
					html += "<td>None</td>"
			else:
				html += "<td>" + str(field) + "</td>"
		html += "</tr>"
	html += "</table>"
	return html
	
	

def ListMomentsByKloudletId(condition):
# @parm condition:		List-Sets		[(field, operator, value),...] (ex. ('Name', '=', 'Ali'))
# @ return json
	# get the required fields
	RQfields = ['ID', 'TYPE', 'TEXT', 'MEDIA_ID', 'BLOBDATA', 'URL', 'GEOLOCATION', 'PARENTID', 'CREATED_BY', 'CREATED_ON']
	rows = MKController.GetMomentsByKloudletId(RQfields, condition)
	
	# yield the HTML
	# yield the HTML 
	html ="<table border='1'><tr>"
	for f in RQfields:
		html += "<td>" + f + "</td>"
	html += "</tr>"
	for row in rows:
		html += "<tr>"
		for i,field in enumerate(row):
			if i == 1: # NAME
				html += "<td><a href='/moment?id=%s'> %s</a></td>" % (row[0],str(field))
			elif i == 4: #BLOBDATA
				filePath = ""
				if row[i] != None:
					filePath = MKUtils.GetSubFolder() + "momentId_" + str(row[0]) + ".jpg"
					# TODO: How to render images instead of strings in the browser?
					with open(filePath, "wb") as output_file:
						output_file.write(row[i])
					html += "<td><a href ='file?url=" + filePath + "'>Image</a></td>"
				else:
					html += "<td>None</td>"
			else:
				html += "<td>" + str(field) + "</td>"
		html += "</tr>"
	html += "</table>"
	return html
	
