#upload images to CDN
from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid
import cv2
import numpy as np

class uploadImage(Resource):
        def post(self):
                try:
                        parser = reqparse.RequestParser()
                        parser.add_argument('path', type=str, help='path to save image')
                        parser.add_argument('size', type=str, help='image resized to this pixel size')
                        args = parser.parse_args()

                        _path = args['path']
                        _size = args['size']

                        if len(_size) > 0:
                                size_list = _size.split(",")
                        else:
                                size_list = ['100%']            #if size is not mentioned, upload original image

                        if _path[-1] == '/':
                                _path = _path[:-1]              #last '/' removed for proper url generation 

                        path_list = _path.split("/")

                        #credentials of cdn server
                        ftp = FTP('push-12.cdn77.com')
                        ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
                        ftp.cwd('/www/images/')

                        dir ='/www/images/'

                        for p in path_list:
                                if p not in ftp.nlst():
                                        ftp.mkd(p)
                                dir = dir + p + '/'
                                ftp.cwd(dir)

                        url_list = []
                        # url='https://1763256174.rsc.cdn77.org/images/'+_path
			url='https://1005776689.rsc.cdn77.org/images/'+_path

                        for key in request.files:
                                uploadedfile = request.files[key]
                                filename = secure_filename(uploadedfile.filename)
                                os.chdir('/var/www/api/knowledgeBase/images')
                                uploadedfile.save(filename)                     #saving file to cwd(current working directory)
                                for size in size_list:
                                        urls = {}
                                        img = cv2.imread(filename,1)            #reading file from cwd
                                        if 'x'in size:
                                                dimension = size.split('x')  
					if 'X' in size:
						dimension=size.split('X')    #if size is in pixels
                                        if '%' in size:
                                                percent = int(size[:-1])/100.0  #if size is in %
                                                height, width, channel = img.shape              #getting original dimensions
                                                dimension = [width*percent, height*percent]
                                        img = cv2.resize(img,(int(dimension[0]),int(dimension[1])))
                                        newName = str(uuid.uuid4())+'.JPEG'
                                        cv2.imwrite(newName,img)                                #saving image with changed name and dimension
                                        ext = os.path.splitext(newName)[1]

                                        #uploading image to CDN
                                        if ext in (".JPEG", ".jpg", ".jpeg",".png",".svg"):
                                                ftp.storbinary("STOR " + newName, open(newName,"rb"), 1024)
                                        else:
                                                return {'StatusCode':'400','Message':'Only image files accepted'}
                                        imageUrl = url+'/'+newName              #generating URL of the image in CDN
                                        os.remove(newName)                      #removing new image from cwd
                                        urls['size'] = size
                                        urls['imageUrl'] = imageUrl
                                        url_list.append(urls)
                                os.remove(filename)                             #remove original image from cwd

                        ftp.quit()
                        return {'SuccessCode':'200', 'URLs':url_list}
                except Exception as e:
                        return {'ErrorCode':'400','Message':str(e)}

