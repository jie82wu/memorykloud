# MKconfig.py
# najjaray@gmail.com (@najjaray)
# Monday, March 5, 2012
# jwu: modified on April 02, 2012

server_port = 8080

dbhost = '23.21.211.104'
dbusername = 'memorykloud'
dbpasswrd = 'ischool12'
dbcatalog = 'memorykloud_dev'

stname = 'MK.status'
lgname = 'MK.log'
FSroot = ''
FSFile = 'files/'

# STATUS DICTIONARY
STATUS = {}
STATUS['REST'] = 0
STATUS['kloudlets'] = 0
STATUS['users'] = 0
STATUS['moments'] = 0
STATUS['files'] = 0
STATUS['/'] = {}
STATUS['/']['GET'] = 0
STATUS['/']['POST'] = 0
STATUS['/']['PUT'] = 0
STATUS['/']['DELETE'] = 0
STATUS['/admin'] = {}
STATUS['/admin']['GET'] = 0
STATUS['/admin']['POST'] = 0
STATUS['/admin']['PUT'] = 0
STATUS['/admin']['DELETE'] = 0
STATUS['/kloudlet'] = {}
STATUS['/kloudlet']['GET'] = 0
STATUS['/kloudlet']['POST'] = 0
STATUS['/kloudlet']['PUT'] = 0
STATUS['/kloudlet']['DELETE'] = 0
STATUS['/user'] = {}
STATUS['/user']['GET'] = 0
STATUS['/user']['POST'] = 0
STATUS['/user']['PUT'] = 0
STATUS['/user']['DELETE'] = 0
STATUS['/moment'] = {}
STATUS['/moment']['GET'] = 0
STATUS['/moment']['POST'] = 0
STATUS['/moment']['PUT'] = 0
STATUS['/moment']['DELETE'] = 0
STATUS['/file'] = {}
STATUS['/file']['GET'] = 0
STATUS['/file']['POST'] = 0
STATUS['/file']['PUT'] = 0
STATUS['/file']['DELETE'] = 0
STATUS['/invite']= {}
STATUS['/invite']['GET'] = 0
STATUS['/invite']['POST'] = 0
STATUS['/invite']['PUT'] = 0
STATUS['/invite']['DELETE'] = 0

STATUS['ERROR 404'] = {}
STATUS['ERROR 404']['GET'] = 0
STATUS['ERROR 404']['POST'] = 0
STATUS['ERROR 404']['PUT'] = 0
STATUS['ERROR 404']['DELETE'] = 0

STATUS['ERROR 500'] = {}
STATUS['ERROR 500']['GET'] = 0
STATUS['ERROR 500']['POST'] = 0
STATUS['ERROR 500']['PUT'] = 0
STATUS['ERROR 500']['DELETE'] = 0
