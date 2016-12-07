from restful import Resource
from flask_restful import reqparse
from random import randint
import requests

class sendOtp(Resource):
        def post(self):
                parser = reqparse.RequestParser()
                parser.add_argument('mobno', type=str, help='mobile number')
                args = parser.parse_args()

                _mobno = args['mobno']

                r = randint(1000, 9999)
                _randno = r
                payload = {'usr': '28221', 'pwd': 'password1', 'ph':_mobno,'sndr': 'IAMFAB', 'text': 'Greetings. ' + str(_randno) +  ' is your FAB2U verification code'}
                r = requests.get('http://bulksms.flyfotservices.com/unified.php', params=payload)
                return {'StatusCode':'200','Message':'OTP sent', 'OTP': str(_randno)}
