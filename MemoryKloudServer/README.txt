- Prerequites for running the applications

	* SimpleJSON: http://pypi.python.org/pypi/simplejson/
	* python-mysqldb: http://mysql-python.sourceforge.net/ http://www.codegood.com/

- How to run the application
	* python MK.py

- Note: Currently the port is hard coded to be 8080 (defined in MKconfig->server_port)

- Following are the available REST URLs:
	* GET (HTML)
		o /: Home Page
		o /admin: Admin Page
		o /user: Show a HTML form where new users can be added (regardless if this page has parameters)
		o /kloudlet: Show a HTML form where new kloudlet can be added (regardless if this page has parameters)
			- /kloudlet?id=all shows all kloudlets
			- /kloudlet?id=? shows a kloudlet given a kloudlet id
		o /moment: Show a HTML form where new moment can be added (regardless if this page has parameters)
			- /moment?id=all shows all moments
			- /moment?id=? shows a moment
			- /moment?kid=? shows all the moments given a kloudlet id
		o /file: Show a HTML form where new file can be added (regardless if this page has parameters) 
			- Note: a file is a moment, it just adds new entries to the mk_media_storage table
			- /file?url=? shows the file
		o /invite: Show a HTML form where new invite can be added (regardless if this page has parameters) 
		
	* GET (JSON)
		o /json/user: = /user
		o /json/user?id=all: a JSON array of all users
		o /json/user?id=?: a JSON array of given user
		o /json/kloudlet: = /kloudlet
		o /json/kloudlet?id=all: a JSON array of all kloudlets
		o /json/kloudlet?id=?: a JSON array of given kloudlet
		o /json/kloudlet?id=all&showcover=true: a JSON array of all kloudlets with their cover page shown
		o /json/kloudlet?id=?&showcover=true: a JSON array of given kloudlet with its cover page shown
		o /json/moment: = /moment
		o /json/moment?id=all: a JSON array of all moments
		o /json/moment?id=?: a JSON array of given moment
		o /json/moment?kid=? a JSON array of all moments for a given kloudlet

	* POST:
		o /user: create a user with the following params: user_fullname, user_email, user_handle 
		o /kloudlet: create a kloudlet with the following params: user_id, kloudlet_name
		o /invite: create an invite with the following params: inviter_id, kloudlet_id, guest_name,guest_email
		o /moment: create an moment with the following params: user_id, kloudlet_id, moment_text
		o /file: create an moment with the following params: user_id, kloudlet_id, file_body, file_name
	
