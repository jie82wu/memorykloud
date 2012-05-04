# MK.py
import MKconfig, MKHTML, MKJSON, MKMySql, MKController, MKUtils
import logging, pickle, sqlite3, datetime, sys, simplejson
import cgi, os,urlparse
import cgitb; cgitb.enable()
# to review imports
import re, operator
import string,time,urllib
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
	
def save_status(stname):
	filehandler = open(stname,'w') 
	pickle.dump(MKconfig.STATUS, filehandler)
	filehandler.close()

class MyHandler(BaseHTTPRequestHandler):
	# Handle GET requests
	def do_GET(self):
		logging.info("GET       | %s %s" % (self.client_address[0], self.path))
		GETquery = urlparse.urlparse(self.path).query
		GETpath = urlparse.urlparse(self.path).path
		GETparam = {}
		GETparms = {}
		
		if len(GETquery) > 0:
			if "&" in GETquery:
				GETparms = GETquery.split('&')
			else:
				GETparms = [GETquery]
				
		for parm in GETparms:
			if "=" in parm:
				key, value = parm.split("=", 2)
				GETparam[key] = value
		try:
			MKconfig.STATUS['REST']+=1
			# MK GET HOME HTML
			if GETpath == "/":
				MKconfig.STATUS['/']['GET'] +=1
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(MKHTML.HomeIndex() +"<hr>"+ MKHTML.ListKloudlets(None))
				return
			elif GETpath == "/favicon.jpg":
				ResponseCode, ContentType, ContentBody = MKUtils.GetFile('favicon.jpg')
				self.send_response( ResponseCode )
				self.send_header( "Content-type", ContentType )
				self.send_header( "Content-length", str(len(ContentBody)) )
				self.end_headers()
				self.wfile.write( ContentBody )
				return
			# MK FER ADMIN HTML
			elif GETpath == "/admin":
				MKconfig.STATUS['/admin']['GET'] +=1
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(MKHTML.AdminIndex())
				return
			# MK GET USER HTML
			elif GETpath == "/user":
				MKconfig.STATUS['/user']['GET'] +=1
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(MKHTML.NewUserForm())
				return
			# MK GET KLOUDLET HTML
			elif GETpath == "/kloudlet":
				MKconfig.STATUS['/kloudlet']['GET'] += 1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':							
							self.send_response(200)
							self.send_header('Content-type',	'text/html')
							self.end_headers()
							self.wfile.write(MKHTML.ListKloudlets(None))
						else:
							self.send_response(200)
							self.send_header('Content-type',	'text/html')
							self.end_headers()
							self.wfile.write(MKHTML.ListKloudlets(([('ID',' = ', str(GETparam['id']))])))
						return
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(MKHTML.NewKloudletForm())
				return
			# MK GET MOMENT HTML
			elif GETpath == "/moment":
				MKconfig.STATUS['/moment']['GET'] +=1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':							
							self.send_response(200)
							self.send_header('Content-type',	'text/html')
							self.end_headers()
							self.wfile.write(MKHTML.ListMoments(None))
						else:
							self.send_response(200)
							self.send_header('Content-type',	'text/html')
							self.end_headers()
							self.wfile.write(MKHTML.ListMoments(([('M.ID',' = ', str(GETparam['id']))])))
						return
					if 'kid' in GETparam.keys():
						self.send_response(200)
						self.send_header('Content-type',	'text/html')
						self.end_headers()
						self.wfile.write(MKHTML.ListMomentsByKloudletId(([('KM.KLOUDLET_ID',' = ', str(GETparam['kid']))])))
						return
				else:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					self.wfile.write(MKHTML.NewMomentForm())
				return
			# MK GET FILE
			elif GETpath == "/file":
				MKconfig.STATUS['/file']['GET'] +=1
				if len(GETparam)>0:
					if 'url' in GETparam.keys():
						ResponseCode, ContentType, ContentBody = MKUtils.GetFile(GETparam['url'])
				else:
					ResponseCode, ContentType, ContentBody = 200, 'text/html', MKHTML.NewFileForm()
				self.send_response(ResponseCode)
				self.send_header('Content-type',ContentType)
				self.end_headers()
				self.wfile.write(ContentBody)
				return
			# MK GET INVITE HTML
			elif GETpath == "/invite":
				MKconfig.STATUS['/invite']['GET'] +=1
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(MKHTML.NewInviteForm())
				return
			# MK GET USER JSON
			elif GETpath == "/json/user":
				MKconfig.STATUS['/user']['GET'] +=1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin', '*')
								self.send_header('Access-Control-Allow-Methods', 'GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListUsers(None))+');')
								return 
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin', '*')
								self.send_header('Access-Control-Allow-Methods', 'GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								self.wfile.write(simplejson.dumps(MKJSON.ListUsers(None)))
								return
						else:
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin', '*')
								self.send_header('Access-Control-Allow-Methods', 'GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'('+simplejson.dumps(MKJSON.ListUsers([('ID',' = ', str(GETparam['id']))]))+");")
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin', '*')
								self.send_header('Access-Control-Allow-Methods', 'GET')
								self.send_header('Content-type','application/json')
								self.end_headers()							
								self.wfile.write(simplejson.dumps(MKJSON.ListUsers([('ID',' = ', str(GETparam['id']))])))
								return
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(MKHTML.NewUserForm())
				return
			# MK GET KLOUDLET JSON
			elif GETpath == "/json/kloudlet":
				MKconfig.STATUS['/kloudlet']['GET'] += 1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								if 'showcover' in GETparam.keys() and GETparam['showcover'].lower() == 'true':
									self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListKloudletsWithCover(None))+');')
								else:
									self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListKloudlets(None))+');')
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								if 'showcover' in GETparam.keys() and GETparam['showcover'].lower() == 'true':
									self.wfile.write(simplejson.dumps(MKJSON.ListKloudletsWithCover(None)))
								else:
									self.wfile.write(simplejson.dumps(MKJSON.ListKloudlets(None)))
								return 
						else:
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								if 'showcover' in GETparam.keys() and GETparam['showcover'].lower() == 'true':
									self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListKloudletsWithCover([('ID',' = ', str(GETparam['id']))]))+");")
								else:
									self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListKloudlets([('ID',' = ', str(GETparam['id']))]))+");")
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								if 'showcover' in GETparam.keys() and GETparam['showcover'].lower() == 'true':
									self.wfile.write(simplejson.dumps(MKJSON.ListKloudletsWithCover([('ID',' = ', str(GETparam['id']))])))
								else:
									self.wfile.write(simplejson.dumps(MKJSON.ListKloudlets([('ID',' = ', str(GETparam['id']))])))
								return
				else:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write(MKHTML.NewKloudletForm())
					return
			# MK GET MOMENTS
			elif GETpath == "/json/moment":
				MKconfig.STATUS['/moment']['GET'] += 1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'(""'+ simplejson.dumps(MKJSON.ListMoments(None))+'");')
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								self.wfile.write(simplejson.dumps(MKJSON.ListMoments(None)))
								return 
						else:
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListMoments([('M.ID',' = ', str(GETparam['id']))]))+");")
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								self.wfile.write(simplejson.dumps(MKJSON.ListMoments([('M.ID',' = ', str(GETparam['id']))])))
								return
					if 'kid' in GETparam.keys():
						if 'callback' in GETparam.keys():
							self.send_response(200)
							self.send_header('Access-Control-Allow-Origin','*')
							self.send_header('Access-Control-Allow-Methods','GET')
							self.send_header('Content-type','application/javascript')
							self.end_headers()
							self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListMomentsByKloudletId([('KM.KLOUDLET_ID',' = ', str(GETparam['kid']))]))+");")
							return
						else:
							self.send_response(200)
							self.send_header('Access-Control-Allow-Origin','*')
							self.send_header('Access-Control-Allow-Methods','GET')
							self.send_header('Content-type','application/json')
							self.end_headers()
							self.wfile.write(simplejson.dumps(MKJSON.ListMomentsByKloudletId([('KM.KLOUDLET_ID',' = ', str(GETparam['kid']))])))
							return
				else:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write(MKHTML.NewMomentForm())
					return
			elif GETpath == "/json/moment2":
				MKconfig.STATUS['/moment']['GET'] += 1
				if len(GETparam)>0:
					if 'id' in GETparam.keys():
						if GETparam['id'].lower() == 'all':
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'(""'+ simplejson.dumps(MKJSON.ListMoments2(None))+'");')
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								self.wfile.write(simplejson.dumps(MKJSON.ListMoments2(None)))
								return 
						else:
							if 'callback' in GETparam.keys():
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/javascript')
								self.end_headers()
								self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListMoments2([('M.ID',' = ', str(GETparam['id']))]))+");")
								return
							else:
								self.send_response(200)
								self.send_header('Access-Control-Allow-Origin','*')
								self.send_header('Access-Control-Allow-Methods','GET')
								self.send_header('Content-type','application/json')
								self.end_headers()
								self.wfile.write(simplejson.dumps(MKJSON.ListMoments2([('M.ID',' = ', str(GETparam['id']))])))
								return
					if 'kid' in GETparam.keys():
						if 'callback' in GETparam.keys():
							self.send_response(200)
							self.send_header('Access-Control-Allow-Origin','*')
							self.send_header('Access-Control-Allow-Methods','GET')
							self.send_header('Content-type','application/javascript')
							self.end_headers()
							self.wfile.write(GETparam['callback'] +'('+ simplejson.dumps(MKJSON.ListMomentsByKloudletId2([('KM.KLOUDLET_ID',' = ', str(GETparam['kid']))]))+");")
							return
						else:
							self.send_response(200)
							self.send_header('Access-Control-Allow-Origin','*')
							self.send_header('Access-Control-Allow-Methods','GET')
							self.send_header('Content-type','application/json')
							self.end_headers()
							self.wfile.write(simplejson.dumps(MKJSON.ListMomentsByKloudletId2([('KM.KLOUDLET_ID',' = ', str(GETparam['kid']))])))
							return
				else:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write(MKHTML.NewMomentForm())
					return
			else:
				MKconfig.STATUS['ERROR 404']['GET'] += 1
				self.send_error(404,'Not Found')
				return 
		except IOError:
			MKconfig.STATUS['ERROR 500']['GET'] += 1
			self.send_error(500,'Internal Server Error')
			return
			
	def do_POST(self):
		logging.info("POST      | %s %s" % (self.client_address[0], self.path))
		GETquery = urlparse.urlparse(self.path).query
		GETpath = urlparse.urlparse(self.path).path
		GETparam = {}
		GETparms = {}
		
		if len(GETquery) > 0:
			if "&" in GETquery:
				GETparms = GETquery.split('&')
			else:
				GETparms = [GETquery]
				
		for parm in GETparms:
			if "=" in parm:
				key, value = parm.split("=", 2)
				GETparam[key] = value
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))            
			if ctype == 'multipart/form-data':
				postvars = cgi.FieldStorage(fp = self.rfile,headers = self.headers,environ={ 'REQUEST_METHOD':'POST' }) 
				upfilename = os.path.split(postvars['file'].filename)[1]
				
			elif ctype == 'application/x-www-form-urlencoded':
				length = int(self.headers.getheader('content-length'))
				postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			else:
				postvars = {}
			MKconfig.STATUS['REST']+=1
			# MK POST HOME
			if self.path == "/":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK POST HOME
				""")
				return
			# MK POST KLOUDLET
			elif self.path == "/kloudlet":
				MKconfig.STATUS['/kloudlet']['POST'] +=1
				if 'UID' in postvars.keys() and 'name' in postvars.keys() and len(postvars['UID'][0])>0 and len(postvars['name'][0])>0:
					new_id = MKController.AddNewKloudlet(postvars['UID'][0], postvars['name'][0])
					if 'callback' in GETparam.keys():
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/javascript')
						self.end_headers()
						self.wfile.write(GETparam['callback'] +'('+simplejson.dumps({"kloudlet_id":new_id})+");")
						return 
					else:
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/json')
						self.end_headers()
						self.wfile.write(simplejson.dumps({"kloudlet_id":new_id}))
						return
				else:
					self.send_error(400, 'Bad Request')
					return
			# MK POST USER
			elif self.path == "/user":
				MKconfig.STATUS['/user']['POST'] +=1
				if 'fullname' in postvars.keys() and 'email' in postvars.keys() and len(postvars['fullname'][0])>0 and len(postvars['email'][0])>0:
					new_id = MKController.AddNewUser(postvars['fullname'][0], postvars['email'][0],postvars['email'][0])
					if 'callback' in GETparam.keys():
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/javascript')
						self.end_headers()
						self.wfile.write(GETparam['callback'] +'('+simplejson.dumps({"user_id:":new_id})+");")
						return 
					else:
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/json')
						self.end_headers()
						self.wfile.write(simplejson.dumps({"user_id:":new_id}))
						return
				else:
					self.send_error(400, 'Bad Request')
					return
			# MK POST INVITE
			elif self.path == "/invite":
				MKconfig.STATUS['/invite']['POST'] +=1
				if 'UID' in postvars.keys() and 'EID' in postvars.keys() and 'new_name' in postvars.keys() and 'new_email' in postvars.keys()and len(postvars['UID'][0])>0 and len(postvars['EID'][0])>0 and len(postvars['new_name'][0])>0 and len(postvars['new_email'][0])>0:
					new_id = MKController.AddNewInvitaion(postvars['UID'][0], postvars['EID'][0], postvars['new_name'][0],postvars['new_email'][0])
					if 'callback' in GETparam.keys():
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/javascript')
						self.end_headers()
						self.wfile.write(GETparam['callback'] +'('+simplejson.dumps({"invitation_id":new_id})+");")
						return 
					else:
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/json')
						self.end_headers()
						self.wfile.write(simplejson.dumps({"invitation_id":new_id}))
						return
				else:
					self.send_error(400, 'Bad Request')
					return
			# MK POST MOMENT
			elif self.path == "/moment":
				MKconfig.STATUS['/moment']['POST'] +=1
				if 'UID' in postvars.keys() and 'EID' in postvars.keys() and 'moment' in postvars.keys() and len(postvars['UID'][0])>0 and len(postvars['EID'][0])>0 and len(postvars['moment'][0])>0:
					new_id = MKController.AddNewMoment(postvars['UID'][0], postvars['EID'][0], postvars['moment'][0])
					if 'callback' in GETparam.keys():
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/javascript')
						self.end_headers()
						self.wfile.write(GETparam['callback'] +'('+simplejson.dumps({"MOMENT_ID":new_id})+");")
						return 
					else:
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/json')
						self.end_headers()
						self.wfile.write(simplejson.dumps({"MOMENT_ID":new_id}))
						return
				else:
					self.send_error(400, 'Bad Request')
					return
			# MK POST FILE
			elif self.path == "/file":
				MKconfig.STATUS['/file']['POST'] +=1
				if 'uid' in postvars.keys() and 'kid' in postvars.keys() and 'file' in postvars.keys() and len(postvars['uid'].value)>0 and len(postvars['kid'].value)>0 and len(postvars['file'].value)>0:
					#print postvars['file']
					new_id = MKController.AddNewFile(postvars['uid'].value, postvars['kid'].value, postvars['descp'].value, postvars['file'].value,upfilename)	
					if 'callback' in GETparam.keys():
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/javascript')
						self.end_headers()
						self.wfile.write(GETparam['callback'] +'('+simplejson.dumps({"media_id":new_id})+");")
						return 
					else:
						self.send_response(200)
						self.send_header('Access-Control-Allow-Origin', '*')
						self.send_header('Access-Control-Allow-Methods', 'GET')
						self.send_header('Content-type','application/json')
						self.end_headers()
						self.wfile.write(simplejson.dumps({"media_id":new_id}))
						return
				else:
					self.send_error(400, 'Bad Request')
					return
			else:
				self.send_error(404,'Not Found')
				return
		except IOError:
			self.send_error(500,'Internal Server Error')
			return

	def do_PUT(self):
		logging.info("PUT      | %s %s" % (self.client_address[0], self.path))
		GETquery = urlparse.urlparse(self.path).query
		GETpath = urlparse.urlparse(self.path).path
		GETparam = {}
		GETparms = {}
		
		if len(GETquery) > 0:
			if "&" in GETquery:
				GETparms = GETquery.split('&')
			else:
				GETparms = [GETquery]
				
		for parm in GETparms:
			if "=" in parm:
				key, value = parm.split("=", 2)
				GETparam[key] = value
		try:
			MKconfig.STATUS['REST']+=1
			# MK PUT HOME
			if self.path == "/":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK PUT HOME
				""")
				return
			# MK PUT Kloudlet
			elif self.path == "/kloudlet":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK PUT Kloudlet
				""")
				return
			# MK PUT USER
			elif self.path == "/user":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK PUT USER
				""")
				return
			# MK PUT MOMENT
			elif self.path == "/moment":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK PUT MOMENT
				""")
				return
			# MK PUT FILE
			elif self.path == "/file":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK PUT FILE
				""")
				return
			else:
				self.send_error(404,'Not Found')
				return
		except IOError:
			self.send_error(500,'Internal Server Error')
			return

	def do_DELETE(self):
		logging.info("DELETE    | %s %s" % (self.client_address[0], self.path))
		GETquery = urlparse.urlparse(self.path).query
		GETpath = urlparse.urlparse(self.path).path
		GETparam = {}
		GETparms = {}
		
		if len(GETquery) > 0:
			if "&" in GETquery:
				GETparms = GETquery.split('&')
			else:
				GETparms = [GETquery]
				
		for parm in GETparms:
			if "=" in parm:
				key, value = parm.split("=", 2)
				GETparam[key] = value
		try:
			MKconfig.STATUS['REST']+=1
			# MK DELETE HOME
			if self.path == "/":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK DELETE HOME
				""")
				return
			# MK DELETE KLOUDLET
			elif self.path == "/kloudlet":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK DELETE KLOUDLET
				""")
				return
			# MK DELETE USER
			elif self.path == "/user":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK DELETE USER
				""")
				return
			# MK DELETE MOMENT
			elif self.path == "/moment":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK DELETE MOMENT
				""")
				return
			# MK DELETE FILE
			elif self.path == "/file":
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write("""
				MK DELETE FILE
				""")
				return
			else:
				self.send_error(404,'Not Found')
				return
		except IOError:
			self.send_error(500,'Internal Server Error')
			return
			
def server():
	running = True
	while running:
		try:
			logging.info('Server----| 127.0.0.1 Starting')
			server = HTTPServer(('', MKconfig.server_port), MyHandler)
			logging.info(' ')
			logging.info('*' * 10 + "MemoryKloud.com"+'*' * 10)
			logging.info('Server----| 127.0.0.1 Started')
			print 'Server----| 127.0.0.1 Started'
			server.serve_forever()
		except KeyboardInterrupt:
			logging.info('Server----| 127.0.0.1 received, shutting down ')
			server.socket.close()
			print 'Server----| 127.0.0.1 received, shutting down server'
			save_status(MKconfig.stname)
			running = False
		except:
			server.socket.close()
			running = False
			logging.info('Server----| 127.0.0.1 Saving status ')
			save_status(MKconfig.stname)
			logging.info('Server----| 127.0.0.1 Connection Closed ')
			logging.info('*' * 35)
		
if __name__ == "__main__":
	# config logging format
	logging.basicConfig(filename=MKconfig.lgname, level=logging.INFO,format='%(asctime)s \t[%(levelname)s] \t%(message)s')

	try: # Windows needs stdio set for binary mode.
		import msvcrt
		msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		msvcrt.setmode (1, os.O_BINARY) # stdout = 1
	except ImportError:
		pass
	
	# load status if exists
	if os.path.isfile(MKconfig.stname):
		filehandler = open(MKconfig.stname,'r') 
		MKconfig.STATUS = pickle.load(filehandler)
		filehandler.close()
	
	# starting the server 
	server()