from restful import Resource
from flask_restful import reqparse
import re
from flask import redirect
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import firedb


class verifyOtp(Resource):
        def post(self):
                parser = reqparse.RequestParser()
                parser.add_argument('mobno', type=str)
                parser.add_argument('otp', type=str)
                args = parser.parse_args()
                _mobno = args['mobno']
                _otp = args['otp']

                fire_otp = firedb.roofpik_connect('verifyMobile/'+str(_mobno)+'/otp', auth = True)

                otps = fire_otp.get()
                if otps:
                        for otp in otps:
                                if otp == _otp:
                                        return {'statusCode':'200', 'message': 'Thank you for verifying your mobile'}
                        return {'statusCode':'400', 'message': 'Invalid code'}
                return {'statusCode':'400', 'message': 'Invalid mobile number'}
