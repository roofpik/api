#upload images to CDN
from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid

class uploadFile(Resource):
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
                                return {'SuccessCode':'400', 'message': 'file type not allowed'}

                        if _path[-1] == '/':
                                _path = _path[:-1]              #last '/' removed for proper url generation 

                        path_list = _path.split("/")

                        #credentials of cdn server
                        ftp = FTP('push-12.cdn77.com')
                        ftp.login(user='user_q9b3n9dp', passwd='wGUSlX8t88FcBtc1D7H1')
                        ftp.cwd('/www/files/')

                        dir ='/www/files/'

                        for p in path_list:
                                if p not in ftp.nlst():
                                        ftp.mkd(p)
                                dir = dir + p + '/'
                                ftp.cwd(dir)

                        url_list = []
                        url='https://1019734038.rsc.cdn77.org/files/'+_path
			
                        for key in request.files:
                                uploadedfile = request.files[key]
                                filename = secure_filename(uploadedfile.filename)
                                os.chdir('/var/www/api/knowledgeBase/files')
                                uploadedfile.save(filename)
                                newName = str(uuid.uuid4()) + '.' + fileExt
                                os.rename(filename, newName)
                                ftp.storbinary("STOR " + newName, open(newName,"rb"), 1024)
                                os.remove(newName)
                                url_list.append(url + '/' + newName)
                        ftp.quit()
                        return {'SuccessCode':'200', 'URLs':url_list}
                except Exception as e:
                        return {'ErrorCode':'400','Message':str(e)}

