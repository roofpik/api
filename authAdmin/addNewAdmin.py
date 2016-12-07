from restful import Resource
from flask_restful import reqparse
import re
import random
import sendgrid
import datetime
import firedb
import socket


def sendMail(email, code, adminid):
	client = sendgrid.SendGridClient("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")
	message = sendgrid.Mail()

	message.add_to(email)
	message.set_from("contact@roofpik.com")
	message.set_subject("[Team Roofpik]Email verification code")
	message.set_html("<html><head></head><body><a href='http://139.162.3.205/admin-web/#/signup?id="+adminid+"&email="+email+"&code="+code+"&opt=0'>Click here</a> to verify your email.</body></html>")
	result = client.send(message)
	if str(result[0]) == '200':
		return True
	return False	


def validateName(name):
	return len(name) <= 40

def validateEmail(email):
	return (re.match(r'.*@.*\..*', email) and len(email) <= 255)

def genActivationCode():
	return '-'.join(str(random.randint(100,999)) for i in range(4))


class addNewAdmin(Resource):

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('fname', type=str)
		parser.add_argument('lname', type=str)
		parser.add_argument('email', type=str)
		parser.add_argument('trackingId', type=str)
		args = parser.parse_args()
		_fname = args['fname']
		_lname = args['lname']
		_email = args['email']
		_id = args['trackingId']

		if not _fname or not validateName(_fname):
			return {'StatusCode':'400', 'Message':'Invalid name'}
		if not _lname or not validateName(_lname):
			return {'StatusCode':'400', 'Message':'Invalid name'}
		if not _email or not validateEmail(_email):
			return {'StatusCode':'400', 'Message':'Invalid email'}
		
		fire1 = firedb.roofpik_connect('databaseAccess/admins/write', auth = True)
		fire2 = firedb.roofpik_connect('masterAdmin', auth = True)
		found = 0
		data1 = fire1.get()
		if data1:
			if _id in data1 and data1[_id]:
				found = 1
		if found == 0:
			data2 = fire2.get()
			if data2:
				if _id in data2  and data2[_id]:
					found = 1
		if found == 0:
			return {'StatusCode':'400', 'Message':'You do not have access to this'}

		_code = genActivationCode()
		fire = firedb.roofpik_connect('admins', auth=True)
		admins = fire.get()
		result = 0
#		return 'arpit'
		for admin in admins:
			if admins[admin]['email'] == _email:
				return {'StatusCode':'400', 'Message':'Already registered'}
#		return 'll'
		data = {
			'fname': _fname,
			'lname': _lname,
			'email': _email,
			'trackingId': _id,
			'activeFlag': True,
			'emailFlag': False,
			'mobileFlag': False,
			'createdDate': str(datetime.datetime.now()),
			'verification' : {
				'code' : _code,
				'matchingId' : _email,
				'usedFlag' : False,
				'activeFlag' : True,
				'createdDate' : str(datetime.datetime.now()) 
			}
		}
		result = fire.post(data)
		_admin_id = result['name']
		
		
		if not sendMail(_email, _code, _admin_id):
			return {'StatusCode':'400', 'Message':'Email not sent'}

		
		return {'StatusCode':'200', 'Message':'A mail was sent to the email account with the verification link.', 'TempId':_admin_id}


