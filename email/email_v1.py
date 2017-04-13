# API to filter project list based on various parameters
from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
# import json
# import sendgrid
# from sendgrid.helpers.mail import *
# import templates

# sg = sendgrid.SendGridAPIClient(apikey='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')
# from_email = Email("no-reply@roofpik.com")

class welcomEmail_v1(Resource):
	def post(self):
		try:
			# parser = reqparse.RequestParser()
			# parser.add_argument('email', type=str, help='to email address')
			# parser.add_argument('name', type=str, help='user name')
			# args = parser.parse_args()
			# _email = args['email']
			# _name = args['name']
			# subject = "Welcome to Roofpik "+_name+"!"
			# to_email = Email(_email)
			# content = Content("text/html", templates.welcomeTemplate_v1(_name))
			# mail = Mail(from_email, subject, to_email, content)
			# response = sg.client.mail.send.post(request_body=mail.get())
			return {'status':'200'}
		except Exception as e:
			return {'status':'400','Message':str(e)}
