from restful import Resource
from flask_restful import reqparse
import re
import random
import sendgrid
import datetime
import firedb


class createAdmin(Resource):

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id', type=str)
		parser.add_argument('uid', type=str)

		args = parser.parse_args()
		_id = args['id']
		_uid = args['uid']

		if not _id or not _uid:
			return {'StatusCode':'400', 'Message':'Invalid id'}

		fire = firedb.roofpik_connect('admins/'+_id, auth=True)
		data = fire.get()

		if data:
			data['uid'] = _uid
			data['emailFlag'] = True
			data['verification']['usedFlag'] = True
			data['verification']['activeFlag'] = False
			data['verification']['verifiedDate'] = str(datetime.datetime.now())
		else:
			return {'StatusCode':'400', 'Message':'User does not exist'}
		
		fire.remove()

		fire = firedb.roofpik_connect('admins/'+_uid, auth=True)
		result = fire.put(data)

		return {'StatusCode' : '200', 'Message' : 'Created successfully'}
