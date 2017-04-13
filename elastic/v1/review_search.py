# Get list of reviews of a project based on various filters
from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

class reviewSearch_v1(Resource):
	def get(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('pkey', type=str, help='project key')
			parser.add_argument('userType', type=str, help='Owner, Tenant, Other')
			parser.add_argument('ratings', type=str, help='ratings like 1,2,3')
			parser.add_argument('pagination', type=str, help='page number')
			args = parser.parse_args()
			pkey = args['pkey']
			userType = args['userType']
			ratings = args['ratings']
			pagination = args['pagination']

			query = {}
			query["query"] = {}
			query["query"]["bool"] = {}
			query["query"]["bool"]["must"] = []

			if not pagination:
				pstart = 0
			else:
				pstart = (int(pagination)-1)*10

			query["from"] = pstart
			query["size"] = 10


			if ratings:
				mrfilter = {}
				mrfilter["bool"] = {}
				mrfilter["bool"]["should"] = []

				match = []
				allRatings = ratings.split(',')
				for data in allRatings:
						match.append({"match":{"main.rating":data}})
				mrfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(mrfilter)


			if userType:
				utfilter = {}
				utfilter["bool"] = {}
				utfilter["bool"]["should"] = []

				match = []
				allTypes = userType.split(',')
				for data in allTypes:
						match.append({"match":{"user.type":data}})
				utfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(utfilter)


			pfilter = {}
			pfilter['match'] = {}
			pfilter['match']['project.key'] = pkey

			query["query"]["bool"]["must"].append(pfilter)


			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'
			r = requests.get(esserver + '/allreviewsin/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']

			items = []

			for key in result:
				d = key['_source']
				items.append({
					'name': d['user']['uname'],
					"key": d['main']['key'],
					"rating": d['main']['rating'],
					"details": d['main']['detail'],
					"title": d['main']['title'],
					"date": d['main']['reviewDate']
				  })

			return {'status':'200', 'items': items}
		except Exception as e:
			return {'status':'400','Message':str(e)}



