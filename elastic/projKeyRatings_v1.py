from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

def convert_To_FirstPoint(a):
        return round(a,1)

def calc1(coun,nume):
        if coun!=0 :
                return str(convert_To_FirstPoint(float(nume)/float(coun)))
        else :
                return 'False'

class projKeyRatings_v1(Resource):
        def post(self):
                try:
                        parser = reqparse.RequestParser()
                        parser.add_argument('pkey', type=str, help='project key')
                        args = parser.parse_args()
                        pkey = args['pkey']
                        query = {}
                        query['query'] = {}
                        query['query']['match'] = {}
                        query['query']['match']['project.key'] = pkey
                        query['from'] = 0
                        query['size'] = 400


                        items = []
                        esserver = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com'
                        r = requests.get(esserver + '/allreviewsin/data/_search?', data=json.dumps(query))
                        result = json.loads(r.content)['hits']['hits']
                        count_security=0
                        count_infra=0
                        count_amenities=0
                        count_greenry=0
                        count_parking=0
                        sum_in=0
                        sum_sec=0
                        sum_am=0
                        sum_gr=0
                        sum_prk=0
                        for i in range(0,len(result)):
                                temp=result[i]['_source']['mainrating']
                                if (temp['infrastructure']!=False) :
                                        count_infra += 1
                                        sum_in+=int(temp['infrastructure'])
                                if (temp['security']!=False) :
                                        count_security += 1
                                        sum_sec+=int(temp['security'])
                                if (temp['amenities']!=False) :
                                        count_amenities += 1
                                        sum_am+=int(temp['amenities'])
                                if (temp['greenry']!=False) :
                                        count_greenry += 1
                                        sum_gr+=int(temp['greenry'])
                                if (temp['parking']!=False) :
                                        count_parking += 1
                                        sum_prk+=int(temp['parking'])

                        secur=calc1(count_security,sum_sec)
                        infra=calc1(count_infra,sum_in)
                        amen=calc1(count_amenities,sum_am)
                        green=calc1(count_greenry,sum_gr)
                        prk=calc1(count_parking,sum_prk)
                        count_oth=0
                        count_ten=0
                        count_ow=0
                        countarr=[0,0,0,0,0,0]
                        for i in range(0,len(result)):
                                temp=result[i]['_source']['user']
                                if temp['type']=='Tenant' :
                                        count_ten+=1
                                if temp['type']=='Owner' :
                                        count_ow+=1
                                if temp['type']=='Other' :
                                        count_oth+=1
                                temp1=result[i]['_source']['main']['rating']
                                countarr[temp1-1]+=1
                        calc=0
                        num=0
                        for i in range(0,5):
                                num+=countarr[i]
                                calc+=(i+1)*countarr[i]
                        avg_star=calc1(num,calc)
                        res=[]
                        res.append({
                                        'key':pkey ,
                                        'ratings':
                                                {
                                                        "security_rating": secur,
                                                        "infrastructure_rating": infra,
                                                        "amenities_rating": amen,
                                                        "greenry_rating": green,
                                                        "parking_rating": prk
                                                },
                                        'type':
                                                {
                                                        "owner":count_ow,
                                                        "tenant":count_ten,
                                                        "other":count_oth
                                                },
                                        'star_rating':
                                                {
                                                        "1_star":countarr[0],
                                                        "2_star":countarr[1],
                                                        "3_star":countarr[2],
                                                        "4_star":countarr[3],
                                                        "5_star":countarr[4],
                                                        "avg_star":avg_star
                                                }
                                  })
                        return {'status':'200', 'items': res}
                except Exception as e:
                        return {'status':'400','Message':str(e)}