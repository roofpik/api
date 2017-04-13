from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS


from projects import *
app = Flask(__name__)

mysql.init_app(app)
api = Api(app)
CORS(app)

#Welcome Email
api.add_resource(test, '/test')

if __name__ == "__main__":
	app.debug = True
	app.run()
