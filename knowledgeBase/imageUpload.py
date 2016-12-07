from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid
import cv2
import numpy as np
import base64

class imageUpload(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('path', type='str', help='')
			parser.add_argument('data', type='str')
			args = parser.parse_args()
			_data = args['data']
			_path = args['path']
			newstr = _data.split('base64,')[1]
			#return {'Message': _path}
			imgdata = base64.b64decode(newstr)
			os.chdir('/var/www/api/knowledgeBase')
			filename = str(uuid.uuid4())+'.JPEG'

			#with open(os.path.abspath(os.path.dirname(__file__))+'/'+filename) as f:
			with open(filename, 'wb') as f:
				os.chmod(filename, 0777)
				f.write(imgdata)
				f.close()
		
			ftp = FTP('push-12.cdn77.com')
			ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
			ftp.cwd('/www/images/'+ _path +'/')

			url='https://1005776689.rsc.cdn77.org/images/'+_path+'/'+filename

			ext = os.path.splitext(filename)[1]

			if ext in (".JPEG", ".jpg", ".jpeg",".png",".svg"):
				ftp.storbinary("STOR " + filename, open(filename,"rb"), 1024)
			else:
				return {'StatusCode':'400','Message':'Only image files accepted'}
			os.remove(filename)
			ftp.quit()
			return {'StatusCode': '200', 'Message':url}

		except Exception as e:
			return {'ErrorCode': '400', 'Message': str(e)}
