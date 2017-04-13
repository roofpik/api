from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

class scoresApi(Resource):
        def post(self):
                try:
                        parser = reqparse.RequestParser()
                        parser.add_argument('rkey', type=str, help='random key')
                        parser.add_argument('rtype', type=str, help='random type')
                        args = parser.parse_args()
                        rkey = args['rkey']
                        rtype= args['rtype']
                        query = {}
                        query['query'] = {}
                        query['query']['match'] = {}
                        query['from'] = 0
                        query['size'] = 400
                        if rtype=='city':
                        	query['query']['match']['location.citykey'] = rkey
                        if rtype=='micromarket':
                        	query['query']['match']['location.microkey'] = rkey
                        if rtype=='locality':
                        	query['query']['match']['location.lockey'] = rkey


                        esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com'
                        r = requests.get(esserver + '/projectnewin_v1/data/_search?', data=json.dumps(query))
                        result = json.loads(r.content)['hits']['hits']


                        count_arr1=[0,0,0]
                        count_arr2=[0,0,0]
                        count_arr3=[0,0,0]
                        count_arr4=[0,0,0]
                        count_arr5=[0,0,0]
                        count_arr6=[0,0,0]
                        count_arr7=[0,0,0]
                        count_arr8=[0,0,0]
                        
                        for i in range(0,len(result)):
                        	temp=result[i]['_source']['score']
                        	vall=result[i]['_source']['propType']
                        	if temp['affordable']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				count_arr1[0]+=1
                        			if j=='penthouse' :
                        				count_arr1[1]+=1
                        			if j=='villa' :
                        				count_arr1[2]+=1
                        	if temp['bachelors'] >= 7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr2[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr2[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr2[2]+=1
                        	if temp['bestAmenities']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr3[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr3[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr3[2]+=1
                        	if temp['downtown']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr4[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr4[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr4[2]+=1
                        	if temp['luxury']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr5[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr5[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr5[2]+=1
                        	if temp['petFriendly']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr6[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr6[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr6[2]+=1
                        	if temp['seniorLiving']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr7[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr7[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr7[2]+=1
                        	if temp['ultraLuxury']>=7 :
                        		for j in vall:
                        			if j=='apartment' :
                        				if vall[j]== True :
                        					count_arr8[0]+=1
                        			if j=='penthouse' :
                        				if vall[j]== True :
                        					count_arr8[1]+=1
                        			if j=='villa' :
                        				if vall[j]== True :
                        					count_arr8[2]+=1

						res=[]
                        res.append({


                        				"affordable": {
                        								"apartment":count_arr1[0],
                        								"penthouse":count_arr1[1],
                        								"villa":count_arr1[2]
                        				
                        				},
                        				"bachelors": {
                        								"apartment":count_arr2[0],
                        								"penthouse":count_arr2[1],
                        								"villa":count_arr2[2]

                        				},
                        				"bestAmenities" :{
                        								"apartment":count_arr3[0],
                        								"penthouse":count_arr3[1],
                        								"villa":count_arr3[2]

                        				},
                        				"downtown" :{
                        								"apartment":count_arr4[0],
                        								"penthouse":count_arr4[1],
                        								"villa":count_arr4[2]

                        				},
                        				"luxury" :{
                        								"apartment":count_arr5[0],
                        								"penthouse":count_arr5[1],
                        								"villa":count_arr5[2]

                        				},
                        				"petFriendly":{
                        								"apartment":count_arr6[0],
                        								"penthouse":count_arr6[1],
                        								"villa":count_arr6[2]

                        				},
                        				"seniorLiving":{
                        								"apartment":count_arr7[0],
                        								"penthouse":count_arr7[1],
                        								"villa":count_arr7[2]

                        				},
                        				"ultraLuxury":{
                        								"apartment":count_arr8[0],
                        								"penthouse":count_arr8[1],
                        								"villa":count_arr8[2]

                        				}

                        	})
                        return {'status':'200', 'items': res}
                except Exception as e:
                        return {'status':'400','Message':str(e)}

                        	




