from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
import base64
import os
import uuid
import cv2

class imgUpload(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('path', type=str, help='path to save image')
	    parser.add_argument('img', type=str, help='image src (base64)')
	    parser.add_argument('imgType', type=str, help="image type")
	    parser.add_argument('imgName', type=str, help="image name")
	    parser.add_argument('server', type=str, help="test or fab2u")
            args = parser.parse_args()
            _path = args['path']
	    _img = args['img']
	    _imgType = args['imgType']
	    _imgName = args['imgName']
	    _server = args['server']

	    if not _path:
		_path = 'uploadedImages'
	    if not _img:
		return {'status':'400','Message':'Image file is not valid'}
	    if not _imgType:
		_imgType = 'general'
	    if not _imgName:
		_imgName = str(uuid.uuid4())
	    if not _server:
		_server = 'fab2u'
			
	    dim = []

            if(_imgType == 'profile'):
                dim = [['xs',32,32],['s',64,64],['m',256,256],['l',512,512]]
            elif(_imgType == 'blog'):
                dim = [['xs',45,30],['s',300,200],['m',700,500],['l',1500,1000]]
            elif(_imgType == 'vendor'):
                dim = [['xs',30,45],['s',200,300],['m',500,750],['l',1000,1500]]
            elif(_imgType == 'general'):
                dim = [['xs',30,45],['s',200,300],['m',500,750],['l',1000,1500]]
            else:
                return {'status':'400','Message':'Image type is not valid'}

            _fileName = _imgName + '.jpg'
            imgstr = _img.split('base64,')[1]
            imgdata = base64.b64decode(imgstr)
            os.getcwd()
            os.chdir('/var/www/api/upload/images/')
            with open(_fileName, 'wb') as f:
                f.write(imgdata)
                f.close()
	    _path = _server + '/' + _path
            ftp = FTP('push-20.cdn77.com')
            ftp.login(user='user_s1k6fwa1', passwd='bH0v05LZkpYzlG460ZfO')
	    createPath(ftp, _path)
	    cdnImgUpload(ftp, cv2, _fileName, _imgName, _path, os, dim)
	    ftp.quit()
	    return {'status':'200', 'imageName': _imgName}
        except Exception as e:
            return {
            	'status':'400',
            	'Message':str(e)
            }

def createPath(ftp, _path):
    ftp.cwd('/www/')
    path_list = _path.split("/")
    dir='/www/'
    for p in path_list:
        if p not in ftp.nlst():
            ftp.mkd(p)
        dir = dir + p + '/'
        ftp.cwd(dir)
def cdnImgUpload(ftp, cv2, _fileName, _imgName, _path, os, dim):
    url = ''
    orig_img = cv2.imread(_fileName,1)
    origHeight, origWidth = orig_img.shape[:2]
    for size in dim:
        imgHeight, imgWidth = setSize(origHeight, origWidth, size[1], size[2])
        img_resize = cv2.resize(orig_img,(imgWidth, imgHeight))
        resizeImgName = _imgName+'-'+size[0]+'.jpg'
        cv2.imwrite(resizeImgName, img_resize)
        ftp.storbinary("STOR " + resizeImgName, open(resizeImgName,"rb"), 1024)
        url = url + 'url[]=/fab2u/' + _path + '/' + resizeImgName + '&'
    ftp.storbinary("STOR " + _fileName, open(_fileName,"rb"), 1024)
    url = url + 'url[]=/fab2u/' + _path + '/' + _fileName
    purgeImages(url, os)
def setSize(origHeight, origWidth, height, width):
    if(origHeight > height and origWidth > width):
        return height, width
    else:
        return origHeight, origWidth
def purgeImages(url, os):
    r = os.system('curl --data "cdn_id=61811&login=contact@fab2u.com&passwd=bH0v05LZkpYzlG460ZfO%s" https://api.cdn77.com/v2.0/data/purge' % (url))
