import requests
import json

def genurl(_code):
	url = "https://www.googleapis.com/urlshortener/v1/url"
	querystring = {"key":"AIzaSyD3X69EGJXMiOZPKkRlOQnH2eCNJT5Ne8Q"}
	payload = json.dumps({'longUrl':'http://www.roofpik.com/coupon/activate/'+_code})
	headers = {
	    'content-type': "application/json",
	    }
	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
	return json.loads(response.text.id)




