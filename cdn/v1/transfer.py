from ftplib import FTP
import base64
import os
import requests
import json
import os
import cv2



def createPath(path):
    try:
        _path = path.rstrip('/')
        path_list = _path.split('/')

        # credentials of cdn server

        ftp = FTP('push-12.cdn77.com')
        ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
        ftp.cwd('/www/image/')
        dir = '/www/image/'

        # creating path if not exists

        for p in path_list:
            if p not in ftp.nlst():
                ftp.mkd(p)
            dir = dir + p + '/'
            ftp.cwd(dir)
        ftp.quit()
        return {'status': '200'}
    except Exception, e:
        print e


def imageSize(_imgType, _imgCat):
    if _imgType == 'nearby':
        return [['xs', 30, 45], ['s', 100, 150], ['m', 400, 600], ['l',800, 1200], ['xl', 1200, 1800]]
    if _imgType == 'story':
        return [['xs', 30, 45], ['s', 100, 150], ['m', 400, 600], ['l',800, 1200], ['xl', 1200, 1800]]
    if _imgType == 'residential':
      if _imgCat == 'thumbnail':
        return [['xs', 20, 24], ['s', 100, 120], ['m', 400, 480], ['l',800, 960], ['xl', 1200, 1440]]
      if _imgCat == 'cover':
        return [['xs', 25, 50], ['s', 100, 200], ['m', 400, 800], ['l',800, 1600], ['xl', 1200, 2400]]
      else:
        return [['xs', 30, 45], ['s', 100, 150], ['m', 400, 600], ['l',800, 1200], ['xl', 1200, 1800]]



def setSize(origHeight,origWidth,height,width):
    if origHeight > height and origWidth > width:
        return (height, width)
    else:
        return (origHeight, origWidth)


def postData(key):
    try:
        url = 'https://roofpik-new.firebaseio.com/images/' + key + '/cdn.json'
        val = json.dumps(True)
        r = requests.put(url, val)
    except Exception, e:
        print e


def imageUpload():
    r = requests.request('get','https://roofpik-new.firebaseio.com/images/.json')
    data = r.json()
    os.getcwd()
    err = {}
    os.chdir('images/')
    ftp = FTP('push-12.cdn77.com')
    ftp.login(user='user_o85l0jln', passwd='4J961952nvftlkGLVHGC')
    for key in data:
        d = data[key]
        try:
            print 'step1'
            if d['cdn'] == False:
                print d
                print 'step2', d['imgType'], d['imgCat']
                pathStatus = createPath(d['path'])
                print 'step3'
                if pathStatus['status'] == '200':
                    print d['imgName']
                    ftp.cwd('/www/image/' + d['path'])
                    tempName = d['imgName'] + '.jpg'
                    orig_img = cv2.imread(tempName, 1)
                    (origHeight, origWidth) = orig_img.shape[:2]
                    dim = imageSize(d['imgType'], d['imgCat'])
                    for size in dim:
                        (imgHeight, imgWidth) = setSize(origHeight, origWidth, size[1], size[2])
                        img_resize = cv2.resize(orig_img, (imgWidth,imgHeight))
                        resizeImgName = d['imgName'] + '-' + size[0] + '.jpg'
                        cv2.imwrite(resizeImgName, img_resize)
                        ftp.storbinary('STOR ' + resizeImgName, open(resizeImgName, 'rb'), 1024)
                    postData(key)
        except Exception as e:
            err[key] = True
    ftp.quit()
    print err

imageUpload()

