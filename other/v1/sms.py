from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json
from random import randint
import urllib
import urlshort


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class sendOtp_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('mobile', type=str, help='mobile number')
			args = parser.parse_args()
			_mobile = str(args['mobile'])
			_otp = str(random_with_N_digits(4))
			url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=rNfGwBJ7xcV&MobileNo='+_mobile+'&SenderID=ROOFPK&Message=Greetings! '+_otp+' is your verification code for Roofpik.&ServiceName=TEMPLATE_BASED'
			response = requests.post(url)
			return {'status':'200', 'otp': _otp}
		except Exception as e:
			return {'status':'400','Message':str(e)}

class welcomeSms_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('mobile', type=str, help='mobile number')
			parser.add_argument('name', type=str, help='customer name')
			args = parser.parse_args()
			_mobile = str(args['mobile'])
			_name = str(args['name'])
			f = { 'APIKEY' : 'rNfGwBJ7xcV', 'MobileNo' :_mobile, 'SenderID':'ROOFPK', 'Message':"Welcome! "+_name+ " to Roofpik.com, world's first property reviewing website.",'ServiceName': 'TEMPLATE_BASED'}
			url = "http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx"
			f = urllib.urlencode(f)
			response = requests.post(url, params= f)
			return {'status':'200'}
		except Exception as e:
			return {'status':'400','Message':str(e)}

class writeReviewSms_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('mobile', type=str, help='mobile number')
			args = parser.parse_args()
			_mobile = str(args['mobile'])
			f = { 'APIKEY' : 'rNfGwBJ7xcV',
			'MobileNo' :_mobile,
			'SenderID':'ROOFPK',
			'Message':"Thank you for contributing Arpit! you are now eligible to avail exciting offers from our partners.",
			'ServiceName': 'TEMPLATE_BASED'}
			url = "http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx"
			f = urllib.urlencode(f)
			response = requests.post(url, params= f)
			return {'status':'200'}
		except Exception as e:
			return {'status':'400','Message':str(e)}


class coupon_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('mobile', type=str, help='mobile number')
			parser.add_argument('coupon', type=str, help='coupon code')

			args = parser.parse_args()
			_mobile = str(args['mobile'])
			_coupon = str(args['coupon'])

			f = { 'APIKEY' : 'rNfGwBJ7xcV',
			'MobileNo' :_mobile,
			'SenderID':'ROOFPK',
			'Message':"Your coupon code is " + _coupon +". "+ urlshort.genurl(_coupon),
			'ServiceName': 'TEMPLATE_BASED'}
			url = "http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx"
			f = urllib.urlencode(f)
			response = requests.post(url, params= f)
			return {'status':'200'}
		except Exception as e:
			return {'status':'400','Message':str(e)}