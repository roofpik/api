from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

class searchLocation(Resource):
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
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'
			r = requests.get(esserver + '/locationin/data/_search?', data=json.dumps(query))
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
				r = requests.get(esserver + '/locationin/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					items.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })

				value = json.dumps({'data': sorted(items, key=lambda x: x['score'], reverse=True)})
				jdata = json.loads(value)
			return {'status':'200', 'items': jdata['data']}
		except Exception as e:
			return {'status':'400','Message':str(e)}


class mainSearch(Resource):
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
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'
			r = requests.get(esserver + '/gensearchin/data/_search?', data=json.dumps(query))
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

				r = requests.get(esserver + '/gensearchin/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "url":key['_source']['url'], "score": key['_score'] })
		
			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			return {'status':'200', 'items': jdata['data']}
		except Exception as e:
			return {'status':'400','Message':str(e)}


class mainSearchByLoc(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('val', type=str, help='search string')
			parser.add_argument('lockey', type=str, help='loction key')
			parser.add_argument('loctype', type=str, help='loction type like locality, micromarket or city')
			args = parser.parse_args()
			_val = args['val']
			_loc = args['lockey']
			_type = args['loctype']

			query = {
			   "query": {
			      "bool": {
			         "must": [
			            {
			               "simple_query_string": {
			                  "fields":  ["name^1.5","keyword"],
			                  "query": "*"+_val+"*"
			               }
			            },
			            {
			               "match": {
			                  _type: _loc
			               }
			            }
			         ]
			      }
			   },
	            "from":0,
	            "size":6
			}

			data = []
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'
			r = requests.get(esserver + '/gensearchin/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']
			for key in result:
				data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })

			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)

			if data == []:
				query = {
				   "query": {
				      "bool": {
				         "must": [
				            {
				               "fuzzy" : { "keyword" : {"value" : _val, "fuzziness" :     5}}
				            },
				            {
				               "match": {_type: _loc}
				            }
				         ]
				      }
				   },
		            "from":0,
		            "size":6
				}
				r = requests.get(esserver + '/gensearchin/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']
				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })
				value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
				jdata = json.loads(value)

			return {'status':'200', 'data': jdata}
		except Exception as e:
			return {'status':'400','Message':str(e)}


class projLocSearch(Resource):
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
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'
			r = requests.get(esserver + '/projlocin/data/_search?', data=json.dumps(query))
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

				r = requests.get(esserver + '/projlocin/data/_search?', data=json.dumps(query))
				result = json.loads(r.content)['hits']['hits']

				for key in result:
					data.append({'name': key['_source']['name'], "key": key['_source']['key'], "category":key['_source']['category'], "score": key['_score'] })
			value = json.dumps({'data': sorted(data, key=lambda x: x['score'], reverse=True)})
			jdata = json.loads(value)
			return {'status':'200', 'items': jdata}
		except Exception as e:
			return {'status':'400','Message':str(e)}
