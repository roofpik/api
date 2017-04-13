from flask import request
from restful import Resource
from flask_restful import reqparse
import os


class deleteImage(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('imgName', type=str, help='name of image')
		args = parser.parse_args()

		_imgName = args['imgName']

		os.getcwd()
		os.chdir('/var/www/api/upload/images/')
		os.remove(_imgName)

		return {'status':'200'}
