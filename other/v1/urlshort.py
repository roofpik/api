from flask import request
from restful import Resource
from flask_restful import reqparse
import requests
import json

class shorturl_v1(Resource):
	def post(self):
		try:
			url = "https://www.googleapis.com/urlshortener/v1/url"
			querystring = {"longUrl":"http://www.roofpik.com","key":"AIzaSyD3X69EGJXMiOZPKkRlOQnH2eCNJT5Ne8Q"}
			headers = {
			'content-type': "application/json"
			}
			response = requests.request("POST", url, headers=headers, params=querystring)
			return {'status':response.text}
		except Exception as e:
			return {'status':'400','Message':str(e)}



