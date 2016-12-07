from restful import Resource
from flask_restful import reqparse
from random import randint
import requests
import firedb

class mobileVerify(Resource):
		def post(self):
			parser = reqparse.RequestParser()
			parser.add_argument('mobno', type=str, help='mobile number')
			parser.add_argument('uname', type=str, help='name ')
			parser.add_argument('uemail', type=str, help='email ')
			parser.add_argument('uaddress', type=str, help='address')
			args = parser.parse_args()

			_mobno = args['mobno']
			_uname = args['uname']
			_uemail = args['uemail']
			_uaddress = args['uaddress']

			r = randint(1000, 9999)
			_randno = r
			data  = {
					'mobno': _mobno,
					'name': _uname,
					'email': _uemail,
					'address': _uaddress,
					'otp':{
						str(_randno): True
					}
			}
			

			fire_verify  = firedb.roofpik_connect('verifyMobile/'+str(_mobno), auth = True)
			fire_verify.put(data)

  			payload = {'APIKEY': 'rNfGwBJ7xcV', 'MobileNo': _mobno, 'SenderID':'ROOFPK', 'ServiceName': 'TEMPLATE_BASED','Message': 'Greetings! ' + str(_randno) +  ' is your verification code for Roofpik.'}
			r = requests.get('http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx', params=payload)
			return {'StatusCode':'200','Message':'OTP sent', 'OTP': str(_randno)}


