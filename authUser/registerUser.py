from restful import Resource
from flask_restful import reqparse
import re
import random
import datetime
import md5
import firedb
import string
import time

def genActivationCode():
        return '-'.join(str(random.randint(1000,9999)) for i in range(4))

def genReferralCode(uname):
        charname = uname[:4]
        lenchar = 4 - len(charname)
        chars = ''
        if lenchar > 0:
                chars = "".join( [random.choice(string.letters) for i in xrange(lenchar)] )
        return charname.lower()+chars.lower()+str(random.randint(1000,9999))

class registerUser(Resource):

        def post(self):
                parser = reqparse.RequestParser()
                parser.add_argument('uid', type=str)
                parser.add_argument('mobno', type=str, help='mobile number')
                parser.add_argument('uname', type=str, help='name ')
                parser.add_argument('uemail', type=str, help='email ')
                parser.add_argument('uaddress', type=str, help='address')
                parser.add_argument('deviceId', type=str, help='device Id')
                parser.add_argument('referralCode', type=str)

                args = parser.parse_args()
                _uid = args['uid']
                _mobno = args['mobno']
                _uname = args['uname']
                _uemail = args['uemail']
                _uaddress = args['uaddress']
                _device = args['deviceId']
                _referralCode = args['referralCode']

                _code = genActivationCode()
                _my_referral_code = genReferralCode(_uname)

                if _uaddress:
                        _addressFlag = True
                else:
                        _addressFlag = None

                

                data = {
                        'uid' : _uid,
                        'name' : _uname,
                        'createdTime' : int(time.time()),
                        'activeFlag' : True,
                        'deviceId': _device,
                        'myReferralCode' : _my_referral_code,
                        'referralCode': _referralCode,
                        'address': _uaddress,
                        'addressFlag': _addressFlag,
                        'email' : {
                                'userEmail' : _uemail,
                                'code' : _code,
                                'verifiedFlag' : False
                        },
                        'mobile' : {
                                'mobileNum' : _mobno,
                                'verifiedFlag': True
                        }
                }

                # return data

                

                fire_users  = firedb.roofpik_connect('testusers/data/'+_uid, auth = True)
                fire_users.put(data)
