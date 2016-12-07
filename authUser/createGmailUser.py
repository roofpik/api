from restful import Resource
from flask_restful import reqparse
import re
import random
import datetime
import md5
import firedb

def validateEmail(email):
	return re.match(r'.*@.*\..*', email)

def validatePhone(phone):
	return (re.match(r'\d{10}', phone))

class createGmailUser(Resource):

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('uid', type=str)
		parser.add_argument("name", type=str)
		parser.add_argument("mobileNum", type=str)
		parser.add_argument("email", type=str)

		args = parser.parse_args()
		_uid = args['uid']
		_name = args['name']
		_mobileNum = args['mobileNum']
		_email = args['email']

		if not all([_uid, _name, _mobileNum, _email]):
			return {'StatusCode':'400', 'Message':'Please enter all the required details'}
		if not validateEmail(_email):
			return {'StatusCode':'400', 'Message':'Invalid email'}
		if not validatePhone(str(_mobileNum)):
			return {'StatusCode':'400', 'Message':'Invalid mobile number'}

		data = {
			'name' : _name,
			'createdTime' : str(datetime.datetime.now()),
			'userId': _uid,
			'activeFlag' : True,
			'email' : {
				'userEmail' : _email,
				'activeFlag' : True,
				'emailFlag' : True,
			},
			'mobile' : {
				'mobileNum' : _mobileNum,
				'mobileFlag' : False
			}
		}

		fire  = firedb.roofpik_connect('users/data/'+_uid, auth = True)
		fire.put(data)

		return {'StatusCode':'200', 'Message':'User successfully created'}
