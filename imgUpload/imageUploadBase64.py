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
import base64
class ImageUploadBase64(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('imgType', type=str, required=True, help="image type")
            parser.add_argument('path', type=str, required=True, help="path to store the image")
            parser.add_argument('img', type=str, required=True, help="base64 image data")
            args = parser.parse_args()

            _imgType = args['imgType']
            _path = args['path']
            _img = args['img']

            _imgTypes = ['users', 'feeds', 'vendors', 'general']

            if _imgType not in _imgTypes:
                _imgType = 'general'
    
            _path = _imgType+'/'+_path
            
            dim = [['xs',128], ['s',256], ['m',512], ['l',800], ['xl',1024]]
            
            '''
            If no image name is given create image name
            get the file extension from the data 
            '''
            _imgName = str(uuid.uuid4())

            imgstr = _img.split('base64,')[1]
            imgdata = base64.b64decode(imgstr)
            
            os.getcwd()
            os.chdir('/var/www/api/upload/images/')
            with open(_imgName+'.jpg', 'wb') as f:
                f.write(imgdata)
                f.close()

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

            for size in dim:
                basewidth = float(size[1])
                img = Image.open(_imgName+'.jpg')
                resizeImgName = _imgName+'-'+size[0]+'.jpg'
                
                if basewidth > float(img.size[0]):
                    basewidth = float(img.size[0])
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((int(basewidth), hsize), PIL.Image.ANTIALIAS)
                img.save(resizeImgName)

                ftp.storbinary("STOR " + resizeImgName, open(resizeImgName,"rb"), 1024)
                os.remove(resizeImgName)
            # Keep a copy of the original image
            ftp.storbinary("STOR " + _imgName+'.jpg', open(_imgName+'.jpg',"rb"), 1024)
            os.remove(_imgName+'.jpg')
            ftp.quit()
            return {'status':'200', 'imageName':_imgName}
        except Exception as e:
            return {'status': '400', 'msg': str(e)}
