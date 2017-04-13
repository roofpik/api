from flask import request
from restful import Resource
from flask_restful import reqparse
import requests

class test(Resource):
	def post(self):
		try:
			return "arpit"