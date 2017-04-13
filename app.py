from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from test import *
from elastic import *
from email_s import *
from sms import *
from other import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')

api.add_resource(searchLocation_v1,'/v1/searchLocation')
api.add_resource(mainSearch_v1,'/v1/mainSearch')
api.add_resource(mainSearchByLoc_v1,'/v1/mainSearchByLoc')

api.add_resource(sendOtp_v1,'/v1/sendOtp')
api.add_resource(welcomeSms_v1,'/v1/welcomeSms')
api.add_resource(writeReviewSms_v1,'/v1/writeReviewSms')

api.add_resource(reviewSearch_v1,'/v1/reviewSearch')
api.add_resource(projectFilter_v1,'/v1/projectFilter')
api.add_resource(projKeyRatings_v1,'/v1/projKeyRatings')


api.add_resource(emailWelcome_v1,'/v1/emailWelcome')
api.add_resource(emailReview_v1,'/v1/emailReview')


api.add_resource(shorturl_v1,'/v1/shorturl')


if __name__ == "__main__":
	app.debug = True
	app.run()