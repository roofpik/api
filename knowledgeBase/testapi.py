from flask import request
from restful import Resource
from flask_restful import reqparse

class testapi(Resource):
    def post(self):
        return 'abc'
