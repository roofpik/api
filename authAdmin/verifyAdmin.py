from restful import Resource
from flask_restful import reqparse
import re
from flask import redirect
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import firedb


def validateCode(code):
	return re.match(r'\d{3}-\d{3}-\d{3}-\d{3}', code)


class verifyAdmin(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('adminId', type=str)
		parser.add_argument('code', type=str)
		parser.add_argument('opt', type=str)
		parser.add_argument('matchId', type=str)
		args = parser.parse_args()
		_admin_id = args['adminId']
		_code = args['code']
		_opt = args['opt']
		_match_id = args['matchId']

		if not _admin_id or not _match_id or not _opt:
			return False

		if not _code or not validateCode(_code):
			return False
		validOpts = ['0', '1']
		if str(_opt) not in validOpts:
			return False

		fire = firedb.roofpik_connect('admins/'+_admin_id+'/verification', auth=True)
		data = fire.get()
		
		if data:
			if data['code'] == _code and data['matchingId'] == _match_id and data['activeFlag'] is True:
				return True

		return False



		# _secretKey = 'the quick brown fox jumps over the lazy dog'
		# s = Serializer(_secretKey)
		# _tok = s.dumps({'admin_id': _admin_id, 'ver_id':_ver_id, 'opt':_opt})
		# return redirect("http://127.0.0.1:3000/#/setPassword?hash="+_tok)
