from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
import base64
import os
import uuid
import cv2
import numpy as np

class uploadImage_v1(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('img', type=str, help='image src')
            parser.add_argument('imgName', type=str, help="image name")
            args = parser.parse_args()

            _img = args['img']
            _imgName = args['imgName']
            if not _img:
                return {'status':'400','Message':'Image is not valid'}


            _fileName = _imgName + '.jpg'
            imgstr = _img.split('base64,')[1]
            imgdata = base64.b64decode(imgstr)
            os.getcwd()
            os.chdir('/var/www/api/cdn/v1/images/')
            with open(_fileName, 'wb') as f:
                f.write(imgdata)
                f.close()

            return {'status':'200', 'imageName': _imgName}
        except Exception as e:
            return {'status':'400','Message':str(e)}


class deleteImage_v1(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imgName', type=str, help='name of image')
        args = parser.parse_args()

        _imgName = args['imgName']

        os.getcwd()
        os.chdir('/var/www/api/cdn/v1/images/')
        os.remove(_imgName)

        return {'status':'200'}
