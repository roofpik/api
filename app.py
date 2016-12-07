from flask import Flask
from flask_restful import Api
from flask.ext.mysql import MySQL
from flask.ext.cors import CORS

from knowledgeBase import *
from authAdmin import *
from authUser import *
from projects import *

mysql = MySQL()
app = Flask(__name__)
app.config.from_pyfile('settings.py')

mysql.init_app(app)
api = Api(app)
CORS(app)

#api.add_resource(searchProject, '/searchProject')
#api.add_resorce(imageUpload, '/imageUpload')

#api.add_resource(sendOtp, '/sendOtp')
api.add_resource(testupload,'/testupload')
#api.add_resource(testapi,'/testapi')
api.add_resource(createPath,'/createPath')
api.add_resource(uploadImage, '/uploadImage')
#api.add_resource(uploadFile, '/uploadFile')

api.add_resource(addNewAdmin, '/addNewAdmin')
api.add_resource(verifyAdmin, '/verifyAdmin')
api.add_resource(createAdmin, '/createAdmin')

#api.add_resource(addNewUser, '/addUser')
#api.add_resource(verifyUser, '/verifyUser')
#api.add_resource(createUser, '/createUser')
#api.add_resource(createGmailUser, '/createGmailUser')
#api.add_resource(mobileVerify, '/mobileVerify')
#api.add_resource(resentOtp, '/resentOtp')
#api.add_resource(verifyOtp, '/verifyOtp')
#api.add_resource(registerUser, '/registerUser')
#api.add_resource(newRegistration, '/newRegistration')
#api.add_resource(profileImg, '/profileImg')
if __name__ == "__main__":
	app.debug = True
	app.run()
