# API to filter project list based on various parameters
from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json
from copy import deepcopy

class projectFilter_v1(Resource):
	def post(self):
		try:

			parser = reqparse.RequestParser()
			parser.add_argument('loc', type=str, help='location key')
			parser.add_argument('micro', type=str, help='micromarket key')
			parser.add_argument('ptype', type=str, help='project type like apartment, villa')
			parser.add_argument('bhk', type=str, help='2,3,4 bhk')
			parser.add_argument('rmin', type=str, help='minimum rent')
			parser.add_argument('rmax', type=str, help='maximum rent')
			parser.add_argument('builder', type=str, help='builder key')
			parser.add_argument('category', type=str, help='project category like luxuryliving')
			parser.add_argument('pagination', type=int, help='pagination number')

			args = parser.parse_args()
			loc = args['loc']
			micro = args['micro']
			ptype = args['ptype']
			bhk = args['bhk']
			rmin = args['rmin']
			rmax = args['rmax']
			builder = args['builder']
			category = args['category']
			pagination = args['pagination']


			if not loc:
				loc = ''
			if not micro:
				micro = ''
			if not ptype:
				ptype = 'apartment'
			if not bhk:
				bhk = ''
			if not rmin:
				rmin = ''
			if not rmax:
				rmax = ''
			if not builder:
				builder = ''
			if not category:
				category = ''
			if not pagination:
				pstart = 0
			else:
				pstart = (pagination-1)*20



			query = {}
			query["query"] = {}
			query["query"]["bool"] = {}
			query["query"]["bool"]["must"] = []
			query["sort"] = [{"rank.cityrank" : {"order" : "asc", "mode" : "avg"}}]
			query['from'] = pstart
			query['size'] = 20
			allBhk = ""


			if loc != "":
				lfilter = {}
				lfilter["bool"] = {}
				lfilter["bool"]["should"] = []

				match = []
				allLoc = loc.split(',')
				for data in allLoc:
						match.append({"match":{"location.lockey":data}})
				lfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(lfilter)

			if micro != "":
				mfilter = {}
				mfilter["bool"] = {}
				mfilter["bool"]["should"] = []

				match = []
				allMicro = micro.split(',')
				for data in allMicro:
						match.append({"match":{"location.microkey":data}})
				mfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(mfilter)

			if ptype != "":
				ptypefilter = {}
				ptypefilter["bool"] = {}
				ptypefilter["bool"]["should"] = []

				match = []
				allpType = ptype.split(',')
				for data in allpType:
						match.append({"match":{"propType." + data : "Yes"}})
				ptypefilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(ptypefilter)

			if bhk != "":
				bhkfilter = {}
				bhkfilter["bool"] = {}
				bhkfilter["bool"]["should"] = []

				match = []
				allBhk = bhk.split(',')
				for pitem in allpType:
					for data in allBhk:
							match.append({"match":{"units." + pitem +"."+data : True}})
					bhkfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(bhkfilter)




			if builder != "":
				builderfilter = {}
				builderfilter["bool"] = {}
				builderfilter["bool"]["should"] = []

				match = []
				allBuilder = builder.split(',')
				for data in allBuilder:
						match.append({"match":{"builder.key":data}})
				builderfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(builderfilter)


			if category != "":
				categoryfilter = {}
				categoryfilter["bool"] = {}
				categoryfilter["bool"]["should"] = []

				match = []
				allCategory = category.split(',')
				for data in allCategory:
						match.append({"range":{"score." + data:{"gte" : 7}}})
				categoryfilter["bool"]["should"].append(match)
				query["query"]["bool"]["must"].append(categoryfilter)

			
			if allBhk != "":

				if rmin != "" and rmax == "":


					rminfilter = {}
					rminfilter["bool"] = {}
					rminfilter["bool"]["should"] = []

					rminpfilter = {}
					rminpfilter["bool"] = {}
					rminpfilter["bool"]["must"] = []

					rminsfilter = {}
					rminsfilter["bool"] = {}
					rminsfilter["bool"]["must"] = []

					rmintfilter = {}
					rmintfilter["bool"] = {}
					rmintfilter["bool"]["should"] = []


					for pitem in allpType:
						for data in allBhk:
							rminpfilter["bool"]["must"] = []
							rminsfilter["bool"]["must"] = []
							rmintfilter["bool"]["should"] = []

							rminpfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"gte": rmin}}})
							rminpfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"lte": rmin}}})

							rminsfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"gte": rmin}}})
							
							rmintfilter["bool"]["should"].append(rminpfilter)
							rmintfilter["bool"]["should"].append(rminsfilter)


							rminfilter["bool"]["should"].append(deepcopy(rmintfilter))

					query["query"]["bool"]["must"].append(rminfilter)

				if rmax != "" and rmin == "":


					rmaxfilter = {}
					rmaxfilter["bool"] = {}
					rmaxfilter["bool"]["should"] = []

					rmaxpfilter = {}
					rmaxpfilter["bool"] = {}
					rmaxpfilter["bool"]["must"] = []

					rmaxsfilter = {}
					rmaxsfilter["bool"] = {}
					rmaxsfilter["bool"]["must"] = []

					rmaxtfilter = {}
					rmaxtfilter["bool"] = {}
					rmaxtfilter["bool"]["should"] = []


					for pitem in allpType:
						for data in allBhk:
							rmaxpfilter["bool"]["must"] = []
							rmaxsfilter["bool"]["must"] = []
							rmaxtfilter["bool"]["should"] = []

							rmaxpfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"gte": rmax}}})
							rmaxpfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"lte": rmax}}})

							rmaxsfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"lte": rmax}}})
							
							rmaxtfilter["bool"]["should"].append(rmaxpfilter)
							rmaxtfilter["bool"]["should"].append(rmaxsfilter)

							rmaxfilter["bool"]["should"].append(deepcopy(rmaxtfilter))

					query["query"]["bool"]["must"].append(rmaxfilter)


				if rmin != "" and rmax != "":

					rentfilter = {}
					rentfilter["bool"] = {}
					rentfilter["bool"]["should"] = []

					rentpfilter = {}
					rentpfilter["bool"] = {}
					rentpfilter["bool"]["must"] = []

					rentsfilter = {}
					rentsfilter["bool"] = {}
					rentsfilter["bool"]["must"] = []

					renttfilter = {}
					renttfilter["bool"] = {}
					renttfilter["bool"]["must"] = []

					rentxfilter = {}
					rentxfilter["bool"] = {}
					rentxfilter["bool"]["should"] = []


					for pitem in allpType:
						for data in allBhk:
							rentpfilter["bool"]["must"] = []
							rentsfilter["bool"]["must"] = []
							renttfilter["bool"]["must"] = []
							rentxfilter["bool"]["should"] = []

							rentpfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"lte": rmin}}})
							rentpfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"gte": rmin}}})

							rentsfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"gte": rmin}}})
							rentsfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"lte": rmax}}})

							renttfilter["bool"]["must"].append({"range":{"rentMin." + pitem +"."+data :{"lte": rmax}}})
							renttfilter["bool"]["must"].append({"range":{"rentMax." + pitem +"."+data :{"gte": rmax}}})
							
							rentxfilter["bool"]["should"].append(rentpfilter)
							rentxfilter["bool"]["should"].append(rentsfilter)
							rentxfilter["bool"]["should"].append(renttfilter)


							rentfilter["bool"]["should"].append(deepcopy(rentxfilter))

					query["query"]["bool"]["must"].append(rentfilter)


			else:

				if rmin != "" and rmax == "":

					rminfilter = {}
					rminfilter["bool"] = {}
					rminfilter["bool"]["should"] = []

					rminpfilter = {}
					rminpfilter["bool"] = {}
					rminpfilter["bool"]["must"] = []

					rminsfilter = {}
					rminsfilter["bool"] = {}
					rminsfilter["bool"]["must"] = []

					rmintfilter = {}
					rmintfilter["bool"] = {}
					rmintfilter["bool"]["should"] = []


					for pitem in allpType:

						rminpfilter["bool"]["must"] = []
						rminsfilter["bool"]["must"] = []
						rmintfilter["bool"]["should"] = []

						rminpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"gte": rmin}}})
						rminpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"lte": rmin}}})

						rminsfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"gte": rmin}}})
						
						rmintfilter["bool"]["should"].append(rminpfilter)
						rmintfilter["bool"]["should"].append(rminsfilter)


						rminfilter["bool"]["should"].append(deepcopy(rmintfilter))

					query["query"]["bool"]["must"].append(rminfilter)

				if rmax != "" and rmin == "":


					rmaxfilter = {}
					rmaxfilter["bool"] = {}
					rmaxfilter["bool"]["should"] = []

					rmaxpfilter = {}
					rmaxpfilter["bool"] = {}
					rmaxpfilter["bool"]["must"] = []

					rmaxsfilter = {}
					rmaxsfilter["bool"] = {}
					rmaxsfilter["bool"]["must"] = []

					rmaxtfilter = {}
					rmaxtfilter["bool"] = {}
					rmaxtfilter["bool"]["should"] = []


					for pitem in allpType:
						rmaxpfilter["bool"]["must"] = []
						rmaxsfilter["bool"]["must"] = []
						rmaxtfilter["bool"]["should"] = []

						rmaxpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"gte": rmax}}})
						rmaxpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"lte": rmax}}})

						rmaxsfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"lte": rmax}}})
						
						rmaxtfilter["bool"]["should"].append(rmaxpfilter)
						rmaxtfilter["bool"]["should"].append(rmaxsfilter)

						rmaxfilter["bool"]["should"].append(deepcopy(rmaxtfilter))

					query["query"]["bool"]["must"].append(rmaxfilter)

				if rmin != "" and rmax != "":

					rentfilter = {}
					rentfilter["bool"] = {}
					rentfilter["bool"]["should"] = []

					rentpfilter = {}
					rentpfilter["bool"] = {}
					rentpfilter["bool"]["must"] = []

					rentsfilter = {}
					rentsfilter["bool"] = {}
					rentsfilter["bool"]["must"] = []

					renttfilter = {}
					renttfilter["bool"] = {}
					renttfilter["bool"]["must"] = []

					rentxfilter = {}
					rentxfilter["bool"] = {}
					rentxfilter["bool"]["should"] = []


					for pitem in allpType:

						rentpfilter["bool"]["must"] = []
						rentsfilter["bool"]["must"] = []
						renttfilter["bool"]["must"] = []
						rentxfilter["bool"]["should"] = []

						rentpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"lte": rmin}}})
						rentpfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"gte": rmin}}})

						rentsfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"gte": rmin}}})
						rentsfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"lte": rmax}}})

						renttfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".min" :{"lte": rmax}}})
						renttfilter["bool"]["must"].append({"range":{"projectrent." + pitem +".max" :{"gte": rmax}}})
						
						rentxfilter["bool"]["should"].append(rentpfilter)
						rentxfilter["bool"]["should"].append(rentsfilter)
						rentxfilter["bool"]["should"].append(renttfilter)


						rentfilter["bool"]["should"].append(deepcopy(rentxfilter))

					query["query"]["bool"]["must"].append(rentfilter)

					


			items = []
			esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com'
			r = requests.get(esserver + '/projectnewin_v1/data/_search?', data=json.dumps(query))
			result = json.loads(r.content)['hits']['hits']
			try:
				for key in result:
					d = key['_source']
					items.append({
						'name': d['name'],
						"key": d['key'],
						"style": d["general"]["style"],
						"segment": d["general"]["segment"],
						"rank": d["rank"]["cityrank"],
						"reviews": d["review"]["count"],
						"rating": round(d["review"]["rating"],1),
						"score": round(d["review"]["score"],1),
					 	'builder': d['builder']['name'],
					 	"propType": d['propType'],
					 	'rent': d['general']['rent'],
					 	"ptype": d["general"]["ptype"],
					 	'location': d['location'], 
					 	'thumbnail': d['general']['thumbnail']
					  })
			except Exception as e:
				pass


			return {'status':'200', 'items': items}
		except Exception as e:
			return {'status':'400','Message':str(e)}