import smtplib

def mailid(to, tasK_id, EVENT_NAME,body=None):
#	try:
	gmail_user = 'najjaray@gmail.com'
	gmail_pwd = 'bnolno-2011'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To: %s\nFrom: %s \n' + 'Subject: %s\n' (to, gmail_user,"MK Invitation for "+ EVENT_NAME)
	print header
	msg = header + '\n this is test msg from MK.com \n\n'
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()
	return True
#	except:
#		return False
