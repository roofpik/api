from flask import Flask
from flask_restful import Api
from flask.ext.mysql import MySQL
from flask.ext.cors import CORS

#from knowledgeBase import *
from upload import *
from elastic import *
from auth import *
#from hardik import *
#from elastic_v1 import *
from email_v1 import *


mysql = MySQL()
app = Flask(__name__)
app.config.from_pyfile('settings.py')

mysql.init_app(app)
api = Api(app)
CORS(app)

#api.add_resource(mainSearch, '/mainSearch')
#api.add_resource(searchLocation, '/searchLocation')
#api.add_resource(mainSearchByLoc, '/mainSearchByLoc')
#api.add_resource(projectFilter, '/projectFilter')
#api.add_resource(deleteImage,'/deleteImage')
#api.add_resource(uploadImage,'/uploadImage')
#api.add_resource(sendotp, '/sendotp')
#api.add_resource(projLocSearch, '/projLocSearch')
#api.add_resource(projectSearchKey, '/projectSearchKey')
#api.add_resource(projectSearchReviewSummary, '/projectSearchReviewSummary')
#api.add_resource(reviewSearch, '/reviewSearch')
#api.add_resource(ProjKeyRatings,'/ProjKeyRatings')
#api.add_resource(scoresApi,'/scoresApi')

#version 1 API
# Home page search API
#api.add_resource(searchLocation_v1, '/v1/searchLocation')
#api.add_resource(mainSearch_v1, '/v1/mainSearch')
#api.add_resource(mainSearchByLoc_v1, '/v1/mainSearchByLoc')

#Write Review Search APU
#api.add_resource(projLocSearch_v1, '/v1/projLocSearch')

#Project List Main Filter API
#api.add_resource(projectFilter_v1, '/v1/projectFilter')

#Welcome Email
api.add_resource(welcomeEmail_v1, '/v1/welcomeEmail')

if __name__ == "__main__":
	app.debug = True
	app.run()
