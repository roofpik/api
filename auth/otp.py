from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json
from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class sendotp(Resource):
	def post(self):
		try:

			parser = reqparse.RequestParser()
			parser.add_argument('mobile', type=str, help='search string')
			args = parser.parse_args()
			_mobile = str(args['mobile'])
			_otp = str(random_with_N_digits(4))
			url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=rNfGwBJ7xcV&MobileNo='+_mobile+'&SenderID=ROOFPK&Message=Greetings! '+_otp+' is your verification code for Roofpik.&ServiceName=TEMPLATE_BASED'
			response = requests.post(url)

			return {'status':'200', 'otp': _otp}
		except Exception as e:
			return {'status':'400','Message':str(e)}
