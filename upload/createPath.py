def pathFn(ftp, _path):
	ftp.cwd('/www/')
	path_list = _path.split("/")
	dir='/www/'
	for p in path_list:
		if p not in ftp.nlst():
			ftp.mkd(p)
		dir = dir + p + '/'
		ftp.cwd(dir)
