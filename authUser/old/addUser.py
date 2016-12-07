from restful import Resource
from flask_restful import reqparse
import re
import random
import sendgrid
import datetime
import firedb
import socket
import md5
import string


def sendMail(email, code, userid):
#	return "arpit"
	client = sendgrid.SendGridClient("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")
	message = sendgrid.Mail()

	message.add_to(email)
	message.set_from("contact@roofpik.com")
	message.set_subject("[Team Roofpik]Email verification code")
	message.set_html("<html><head></head><body><a href='http://139.162.3.205/verify-email/#/verify?id="+userid+"&code="+code+"'>Click here</a> to verify your email.</body></html>")
	result = client.send(message)
	if str(result[0]) == '200':
		return True
	return False	


def validateEmail(email):
	return re.match(r'.*@.*\..*', email)

def validatePhone(phone):
	return (re.match(r'\d{10}', phone))

def genActivationCode():
	return '-'.join(str(random.randint(1000,9999)) for i in range(4))

def genReferralCode():
	chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
	return chars+str(random.randint(1000,9999))

class addNewUser(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('email', type=str)
		parser.add_argument('password', type=str)
		parser.add_argument('mobileNum', type=str)
		parser.add_argument('referralCode', type=str)
                parser.add_argument('deviceId', type=str)

		args = parser.parse_args()
		_name = args['name']
		_email = args['email']
		_password = args['password']
		_mobile_num = args['mobileNum']
		_referral_code = args['referralCode']
                _device_id = args['deviceId']
		
		if not all([_name, _email, _password, _mobile_num]):
			return {'StatusCode':'400', 'Message':'Please enter all the required details correctly'}
		if not validateEmail(_email):
			return {'StatusCode':'400', 'Message':'Please enter a valid email address'}
		if not validatePhone(str(_mobile_num)):
			return {'StatusCode':'400', 'Message':'Please enter a 10 digit mobile number'}
	
		fire_users = firedb.roofpik_connect('users/data', auth = True)

		users = fire_users.get()
		if users:
			for user in users:
				if users[user]['email'] == _email:
					return {'StatusCode':'400', 'Message':'This email is already registered'}

		# _password = md5.md5(_password).hexdigest()
		_code = genActivationCode()
		_my_referral_code = genReferralCode()

		data = {
			'name' : _name,
			'password' : _password,
			'createdTime' : str(datetime.datetime.now()),
			'activeFlag' : True,
                        'deviceId': _device_id,
			'referralCode' : _referral_code,
			'myReferralCode' : _my_referral_code,
			'email' : {
				'userEmail' : _email,
				'code' : _code,
				'activeFlag' : True,
				'usedFlag' : False,
				'emailFlag' : False,
				'createdTime' : str(datetime.datetime.now())
			},
			'mobile' : {
				'mobileNum' : _mobile_num,
				'mobileFlag' : False
			}
		}

		result = fire_users.post(data)
		_user_id = result['name']

		sendMail(_email, _code, _user_id)		

		return {'StatusCode':'200', 'Message':'An email has been sent to ' + _email + ' with the verification link.'}


