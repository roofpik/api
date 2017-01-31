#upload images to CDN
from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid

class fileUpload(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='name of file')
            parser.add_argument('path', type=str, help='path to save image')
            args = parser.parse_args()

            _path = args['path']
            _name = args['name']

            dotIndex = _name.rfind('.')
            fileExt = _name[dotIndex+1:]

            allowedExtensions = ['txt', 'xlsx', 'xls', 'docx', 'doc', 'pptx', 'ppt', 'pdf']

            if fileExt not in allowedExtensions:
                raise ValueError("File type not allowed")
            if not request.files:
                raise ValueError("No data found")
            
            if _path[-1] == '/':
                    _path = _path[:-1] #last '/' removed for proper url generation 

            #credentials of cdn server
            ftp = FTP('push-20.cdn77.com')
            ftp.login(user='user_s1k6fwa1', passwd='bH0v05LZkpYzlG460ZfO')
            ftp.cwd('/www/files/')

            dir ='/www/files/'
            path_list = _path.split("/")
            for p in path_list:
                if p not in ftp.nlst():
                    ftp.mkd(p)
                dir = dir + p + '/'
                ftp.cwd(dir)

            url_list = []
            url='http://1272343129.rsc.cdn77.org/files/'+_path

            for key in request.files:
                uploadedfile = request.files[key]
                filename = secure_filename(uploadedfile.filename)
                os.chdir('/var/www/api/upload/files')
                uploadedfile.save(filename)
                newName = str(uuid.uuid4()) + '.' + fileExt
                os.rename(filename, newName)
                ftp.storbinary("STOR " + newName, open(newName,"rb"), 1024)
                os.remove(newName)
                url_list.append(url + '/' + newName)
            ftp.quit()
            return {'SuccessCode':'200', 'URLs':url_list}
        except Exception as e:
            return {'ErrorCode': '400', 'Msg': str(e)} 
