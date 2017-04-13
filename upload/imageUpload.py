from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
import base64
import os
import cdnImg
import createPath
import uuid
import cv2
import numpy as np

class uploadImage(Resource):
	def post(self):
		try:

                        parser = reqparse.RequestParser()
#                        parser.add_argument('path', type=str, help='path to save image')
			parser.add_argument('img', type=str, help='image src')
#			parser.add_argument('imgType', type=str, help="image type")
			parser.add_argument('imgName', type=str, help="image name")
#			parser.add_argument('server', type=str, help="test or roofpik server")
                        args = parser.parse_args()

 #                       _path = args['path']
			_img = args['img']
#			_imgType = args['imgType']
			_imgName = args['imgName']
#			_server = args['server']

#			if not _path:
#				_path = 'uploadedImages'
			if not _img:
				return {'status':'400','Message':'Image is not valid'}
#			if not _imgType:
#				_imgType = 'general'
#			if not _imgName:
#				_imgName = str(uuid.uuid4())
#			if not _server:
#				_server = 'roofpik'
#			
#			dim = imageSize(_imgType)

			_fileName = _imgName + '.jpg'
                        imgstr = _img.split('base64,')[1]
                        imgdata = base64.b64decode(imgstr)
                        os.getcwd()
                        os.chdir('/var/www/api/upload/images/')
                        with open(_fileName, 'wb') as f:
                                f.write(imgdata)
                                f.close()
#			_path = _server + '/' + _path
 #                       ftp = FTP('push-12.cdn77.com')
  #                      ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
#			createPath.pathFn(ftp, _path)
#			cdnImg.upload(ftp, cv2, _fileName, _imgName, _path, os, dim)
#			ftp.quit()
			return {'status':'200', 'imageName': _imgName}
                except Exception as e:
                        return {'status':'400','Message':str(e)}


def imageSize(_imgType):

	if(_imgType == 'profile'):
		return [['xs',32,32],['s',64,64],['m',256,256],['l',512,512]]
	if(_imgType == 'project'):
		return [['xs',30,45],['s',200,300],['m',500,750],['l',1000,1500]]
	if(_imgType == 'coverStory'):
		return [['xs',30,45],['s',200,300],['m',500,750],['l',1000,1500]]
	if(_imgType == 'blogs'):
		return [['xs',30,45],['s',200,300],['m',500,750],['l',1000,1500]]
