from restful import Resource
from flask_restful import reqparse
from ftplib import FTP

class createPath(Resource):
        def post(self):
                try:
                        parser = reqparse.RequestParser()
                        parser.add_argument('path', type=str, help='')
                        args = parser.parse_args()
                        _path = args['path']
                        path_list = _path.split("/")

                        # credentials of cdn server
                        ftp = FTP('push-12.cdn77.com')
                        ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
                        ftp.cwd('/www/images/')

                        dir='/www/images/'

                        # creating path if not exists
                        for p in path_list:
                                if p not in ftp.nlst():
                                        ftp.mkd(p)
                                dir = dir + p + '/'
                                ftp.cwd(dir)

                        ftp.quit()
                        return {'SuccessCode':'200', 'path':dir}
                except Exception as e:
                        return {'ErrorCode':'400','Message':str(e)}

