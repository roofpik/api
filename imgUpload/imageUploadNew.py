#upload images to CDN
from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid
import cv2
import PIL
from PIL import Image

class ImageUpload(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('imgType', type=str, required=True, help="image type")
            parser.add_argument('path', type=str, required=True, help="path to store the image")
            args = parser.parse_args()

            _imgType = args['imgType']
            _path = args['path']
            
            _imgTypes = ['profile', 'blogs', 'vendors', 'general']

            if _imgType not in _imgTypes:
                _imgType = 'general'
            
            _path = _imgType+'/'+_path
            
            if  not request.files:
                raise ValueError("No data found")
            '''
            The following are the images width to be resized to
            Height of the image will be calculated proportional to the image width
            '''
            dim = [['xs',128], ['s',256], ['m',512], ['l',800], ['xl',1024]]

            #credentials of cdn server
            ftp = FTP('push-20.cdn77.com')
            ftp.login(user='user_s1k6fwa1', passwd='bH0v05LZkpYzlG460ZfO')
            ftp.cwd('/www/fab2u/')

            dir ='/www/fab2u/'
            path_list = _path.split("/")
            for path in path_list:
                if path not in ftp.nlst():
                    ftp.mkd(path)
                dir = dir + path + '/'
                ftp.cwd(dir)

            img_list = []
            for key in request.files:
                uploadedfile = request.files[key]
                filename = str(uuid.uuid4())

                os.chdir('/var/www/api/upload/images')
                uploadedfile.save(filename+'.jpg')
                for size in dim:
                    basewidth = float(size[1])
                    img = Image.open(filename+'.jpg')
                    # Resize image only if the original size is greater than the size to be resized.
                    if basewidth > float(img.size[0]):
                        basewidth = float(img.size[0])
                    wpercent = (basewidth / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((int(basewidth), hsize), PIL.Image.ANTIALIAS)
                    resizeImgName = filename+'-'+size[0]+'.jpg'
                    img.save(resizeImgName)
                    ftp.storbinary("STOR " + resizeImgName, open(resizeImgName,"rb"), 1024)
                    os.remove(resizeImgName)
                ftp.storbinary("STOR " + filename+'.jpg', open(filename+'.jpg',"rb"), 1024)
                os.remove(filename+'.jpg')
                img_list.append(filename)
            ftp.quit()
            return {'status':'200', 'urls':img_list}
        except Exception as e:
            return {'status': '400', 'msg': str(e)}
