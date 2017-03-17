

def upload(ftp, cv2, _fileName, _imgName, _path, os, dim):
	url = ''
        orig_img = cv2.imread(_fileName,1)
	origHeight, origWidth = orig_img.shape[:2]
	for size in dim:
		imgHeight, imgWidth = setSize(origHeight, origWidth, size[1], size[2])
		img_resize = cv2.resize(orig_img,(imgWidth, imgHeight))
		resizeImgName = _imgName+'-'+size[0]+'.jpg' 
		cv2.imwrite(resizeImgName, img_resize)
        	ftp.storbinary("STOR " + resizeImgName, open(resizeImgName,"rb"), 1024)
		url = url + 'url[]=/roofpik/' + _path + '/' + resizeImgName + '&'
	ftp.storbinary("STOR " + _fileName, open(_fileName,"rb"), 1024)
	url = url + 'url[]=/roofpik/' + _path + '/' + _fileName
	purgeImages(url, os)

def setSize(origHeight, origWidth, height, width):
	if(origHeight > height and origWidth > width):
		return height, width
	else:
		return origHeight, origWidth

def purgeImages(url, os):
	r = os.system('curl --data "cdn_id=77464&login=arpit@roofpik.com&passwd=AWtHpw2RdkUFg0OxIr8G7EQKVhqv3c6s&%s" https://api.cdn77.com/v2.0/data/purge' % (url))
