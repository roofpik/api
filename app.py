from flask import Flask
from flask_restful import Api
from flask.ext.mysql import MySQL
from flask.ext.cors import CORS

from knowledgeBase import *
from projects import *

mysql = MySQL()
app = Flask(__name__)
app.config.from_pyfile('settings.py')

mysql.init_app(app)
api = Api(app)
CORS(app)

api.add_resource(testupload,'/testupload')
api.add_resource(createPath,'/createPath')

if __name__ == "__main__":
	app.debug = True
	app.run()
