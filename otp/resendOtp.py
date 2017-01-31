from restful import Resource
from flask_restful import reqparse
import requests

class resendOtp(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('mobile', required=True, type=int, help='user phone number')
            parser.add_argument('otp', required=True, type=int,  help='one time password')
            args = parser.parse_args()
            _mobile = args['mobile']
            _otp = args['otp']

            url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=GYQVr2Y59ao&MobileNo='+str(_mobile)+'&SenderID=FABTOU&Message=Greetings. '+str(_otp)+' is your FAB2U verification code.&ServiceName=TEMPLATE_BASED'
            response = requests.post(url)
            status = response.status_code
            content = response.content
            return {
                    'status' : status,
                    'msg': 'OTP successfully sent to '+str(_mobile)
                }
        except Exception as e:
            return str(e)
