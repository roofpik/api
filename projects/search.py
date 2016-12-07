from restful import Resource
from flask_restful import reqparse
import json
import firedb

class searchProject(Resource):

	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('query', type=str)
		args = parser.parse_args()
		_query = args['query'].lower()
		fire = firedb.roofpik_connect('search', auth = True)
		data = fire.get()
		names = {}
		if data:
			for item in data:
				t = data[item]['name'].lower().find(_query)
				if t != -1:
					names[item] = data[item]
			return names
		else:
			return "data not available"

