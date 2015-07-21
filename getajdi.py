#!/usr/bin/python
import os, sys, datetime, urllib

APOD_BASE_URL="http://www.astron.nl/dailyimage/"
APOD_URL=APOD_BASE_URL+"main.php?date="
APOD_HOME="aspod"

APOD_HOME=os.environ['HOME']+"/"+APOD_HOME


def imgext(a):
	for ext in ["jpg","gif","png","tif","tiff","jpeg"]:
		if ext in a:
			return True
	return False

def imgstrip(c):
	csp=c.split('"')
	flag=False
	for cc in csp:
		if flag and "pictures" in cc.lower():
			if imgext(cc.lower()):
				return APOD_BASE_URL+cc
			else:
				return False	
		else:
			flag=False
		if "href" in cc.lower():
			flag=True 

	sys.stderr.write("Something went wrong, quitting")
	sys.exit(3)
if len(sys.argv[1:]) == 1:
	date=sys.argv[1]
else:
	date=datetime.date.today().strftime("%Y%m%d")

def get_img(date):
	baseurl=APOD_URL+date
	
	hf=urllib.urlopen(baseurl)
	if hf.getcode() !=200:
		sys.stderr.write("Something went wrong. URL seems not to exist\n\n")
		sys.stderr.write(str(hf.getcode())+"\n\n")
		sys.exit(2)
	else:
		data=hf.readlines()
	hf.close()
	container=list()

	for lin in data:
		if 'DIV style="font-size:smaller"' in lin:
			container.append(lin)
	if len(container)!=1:
		sys.stderr.write("Case needs to be implemented")
		sys.exit(3)
	im=imgstrip(container[0])
	if im:
		return im
	else:
                date = date[2:]
		prevdat=(datetime.date(int("20"+date[0:2]),int(date[2:4]),int(date[4:6]))-datetime.timedelta(1)).strftime("%Y%m%d")
		return get_img(prevdat)

im=get_img(date)
ext=im[-3:]
urllib.urlretrieve(im,APOD_HOME+"/"+"currentajdi.jpg")
