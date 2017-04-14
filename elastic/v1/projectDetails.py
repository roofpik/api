from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

class projectDetails_v1(Resource):
	def get(self):
		try:

			parser = reqparse.RequestParser()

			parser.add_argument('key', type=str, help='project key')
			args = parser.parse_args()
			_key = args['key']
			query = {
			        "query" : {
        				"constant_score" : {
            				"filter" : {
                				"term" : {
                    				"_id" : _key
                				}
            				}
        				}
    				}
				}
			items = []
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com'
			r = requests.get(esserver + '/projectnewin_v1/data/_search?', data=json.dumps(query))

			result = json.loads(r.content)['hits']['hits']

			# print result
			for key in result:
				items.append({'data': key['_source']})

			# jdata = json.dumps(items)
			return {'status':'200', 'items': items}
		except Exception as e:
			return {'status':'400','Message':str(e)}