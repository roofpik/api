from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json


esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'

# locationKeyword.py is used to create the index in es (locationin_v1)
# API is used to search a lcation by it's name
class searchLocation_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('val', type=str, help='search string')
			args = parser.parse_args()
			_val = args['val']
			query = {
			    "query": {
			        "query_string" : {
			            "fields" : ["name^1.5","keyword"],
			            "query" : "*"+_val+"*"
			        }
			    },
			        "from":0,
			       "size":6
				}
			items = []
			r = requests.get(esserver + '/locationin_v1/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']

			# print result
			for key in result:
				items.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })

			value = json.dumps({'data': sorted(items, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			if items == []:
				query = {
				    "query": {
			       "fuzzy" : { "keyword" : {"value" : _val, "fuzziness" :     5}}
				    },
			            "from":0,
				       "size":6
					}
				r = requests.get(esserver + '/locationin_v1/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					items.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })

				value = json.dumps({'data': sorted(items, key=lambda x: x['score'], reverse=True)})
				jdata = json.loads(value)
			return {'status':'200', 'items': jdata['data']}
		except Exception as e:
			return {'status':'400','Message':str(e)}

# projectKeyword.py is used to create the index in es (gensearchin_v1)
# API is used to search a project by it's name
class mainSearch_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('val', type=str, help='search string')
			args = parser.parse_args()
			_val = "*"+args['val'].strip() + "*"
			query = {
			    "query": {
			        "query_string" : {
			            "fields" : ["name^2","keyword"],
			            "query" : _val
			        }
			    },
			        "from":0,
			       "size":6
				}

			data = []
			r = requests.get(esserver + '/gensearchin_v1/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']

			for key in result:
				data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "url":key['_source']['url'], "score": key['_score'] })

			if data == []:
				query = {
				    "query": {
			       "fuzzy" : { "keyword" : {"value" : _val, "fuzziness" :     5}}
				    },
			            "from":0,
				       "size":6
					}

				r = requests.get(esserver + '/gensearchin_v1/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "url":key['_source']['url'], "score": key['_score'] })
		
			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			return {'status':'200', 'items': jdata['data']}
		except Exception as e:
			return {'status':'400','Message':str(e)}



# projectKeyword.py is used to create the index in es (gensearchin_v1)
# API is used to search a project by it's name and location
class mainSearchByLoc_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('val', type=str, help='search string')
			parser.add_argument('type', type=str, help='location type locality, micromarket')
			parser.add_argument('key', type=str, help='key of location')
			args = parser.parse_args()
			_val = "*"+args['val'].strip() + "*"
			_type = args['type']
			_key = args['key']

			query = {}
			query["query"] = {}
			query["query"]["bool"] = {}
			query["query"]["bool"]["must"] = []
			query["from"] = 0
			query["size"] = 6

			# Locality Filter
			locf = {}
			locf["match"] = {_type:_key}
			query["query"]["bool"]["must"].append(locf)

			#Name Filter
			namef = {}
			namef["query_string"] = {}
			namef["query_string"]["fields"] =  ["name^2","keyword"]
			namef["query_string"]["query"] =  _val
			query["query"]["bool"]["must"].append(namef)

			data = []
			r = requests.get(esserver + '/gensearchin_v1/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']

			for key in result:
				data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "url":key['_source']['url'], "score": key['_score'] })

			if data == []:
				query["query"]["bool"]["must"].pop(1)
				fuzzyf = {}
				fuzzyf["fuzzy"] = {}
				fuzzyf["fuzzy"]["keyword"] = {}
				fuzzyf["fuzzy"]["keyword"]["value"] = _val
				fuzzyf["fuzzy"]["keyword"]["fuzziness"] = 5
				query["query"]["bool"]["must"].append(fuzzyf)
				r = requests.get(esserver + '/gensearchin_v1/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "url":key['_source']['url'], "score": key['_score'] })
		
			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			return {'status':'200', 'items': jdata['data']}
		except Exception as e:
			return {'status':'400','Message':str(e)}


#projLocIn.py is used to create the index in es (projlocin_v1)
# API is used in write reviews which searches both projects and locality by name
class projLocSearch_v1(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('val', type=str, help='search string')
			args = parser.parse_args()
			_val = "*"+args['val'].strip() + "*"
			query = {
			    "query": {
			        "query_string" : {
			            "fields" : ["name^2","keyword"],
			            "query" : _val
			        }
			    },
			        "from":0,
			       "size":30
				}

			data = []
			r = requests.get(esserver + '/projlocin_v1/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']

			for key in result:
				data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'] , "score": key['_score']})

			if data == []:
				query = {
				    "query": {
			       "fuzzy" : { "keyword" : {"value" : _val, "fuzziness" :     5}}
				    },
			            "from":0,
				       "size":30
					}

				r = requests.get(esserver + '/projlocin_v1/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })
			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			return {'status':'200', 'items': jdata}
		except Exception as e:
			return {'status':'400','Message':str(e)}


