import urllib
from bs4 import BeautifulSoup
import inspect

nldas_1_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_NOAH0125_H&version=002&page_size=1&sort_key=start_date"
nldas_1f_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_FORA0125_H&version=002&page_size=1&sort_key=start_date"
gldas_1_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_VIC10_3H&version=001&page_size=1&sort_key=start_date"
gldas2_1_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_NOAH025_3H&version=2.0&page_size=1&sort_key=start_date"
trmm_1_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=TRMM_3B42&version=7&page_size=1&sort_key=start_date"
grace_1_begin = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GRACEDADM_CLSM025NA_7D&version=1.0&page_size=1&sort_key=start_date"

nldas_1 = "https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_NOAH0125_H&version=002&page_size=1&sort_key=-start_date"
nldas_1f = "https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_FORA0125_H&version=002&page_size=1&sort_key=-start_date"
gldas_1 = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_VIC10_3H&version=001&page_size=1&sort_key=-start_date"
gldas2_1 = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_NOAH025_3H&version=2.0&page_size=1&sort_key=-start_date"
trmm_1 = "https://cmr.earthdata.nasa.gov/search/granules?short_name=TRMM_3B42&version=7&page_size=1&sort_key=-start_date"
grace_1 = "https://cmr.earthdata.nasa.gov/search/granules?short_name=GRACEDADM_CLSM025NA_7D&version=1.0&page_size=1&sort_key=-start_date"

# Find url2 from url1
def get_url2(url1):
	urlText1 = urllib.urlopen(url1)
	urlLines1 = urlText1.readlines()
	url2 = ""
	for i in range(len(urlLines1)):
		soup1 = BeautifulSoup(urlLines1[i],'html.parser')
		if soup1.find("location") is not None:
			url2 = soup1.location.getText()
	return url2

# # Find begintime from url1
def get_begintime(url2):
	urlText2 = urllib.urlopen(url2)
	urlLines2 = urlText2.readlines()
	begintime = ""
	for j in range(len(urlLines2)):
		soup2 = BeautifulSoup(urlLines2[j], 'html.parser')
		if soup2.find("beginningdatetime") is not None:
			begintime = soup2.beginningdatetime.getText()
	return begintime

# Find endtime from url1
def get_endtime(url2):
	urlText2 = urllib.urlopen(url2)
	urlLines2 = urlText2.readlines()
	endtime = ""
	for j in range(len(urlLines2)):
		soup2 = BeautifulSoup(urlLines2[j], 'html.parser')
		if soup2.find("endingdatetime") is not None:
			endtime = soup2.endingdatetime.getText()
	return endtime

# Find bounding rectangle coordinates
def get_bounds(url2):
	urlText2 = urllib.urlopen(url2)
	urlLines2 = urlText2.readlines()
	bounds = ""
	for k in range(len(urlLines2)):
		soup2 = BeautifulSoup(urlLines2[k], 'html.parser')
		if soup2.find("northboundingcoordinate"):
			nbound = soup2.northboundingcoordinate.getText()
		if soup2.find("eastboundingcoordinate"):
			ebound = soup2.eastboundingcoordinate.getText()
		if soup2.find("southboundingcoordinate"):
			sbound = soup2.southboundingcoordinate.getText()
		if soup2.find("westboundingcoordinate"):
			wbound = soup2.westboundingcoordinate.getText()
	bounds = "%s, %s, %s, %s" % (nbound, ebound, sbound, wbound) #NESW
	return bounds

# Convert datetime to mm/dd/yyyy
def convert_datetime(datetime):
	day = datetime[8:10]
	month = datetime[5:7]
	year = datetime[:4]
	hour = datetime[11:13]
	minute = datetime[14:16]
	second = datetime[17:19]
	return "%s/%s/%s %s:%s:%s" % (month, day, year, hour, minute, second)

# Get all variables
# NLDAS
nldas_2_begin = get_url2(nldas_1_begin)
nldas_begintime = convert_datetime(get_begintime(nldas_2_begin))
# nldas_begintime = '01/02/1979 00:00:00'
nldas_2 = get_url2(nldas_1)
nldas_endtime = convert_datetime(get_endtime(nldas_2))
nldas_bounds = get_bounds(nldas_2)

# NLDAS Forcing
nldas_2f_begin = get_url2(nldas_1f_begin)
nldasf_begintime = convert_datetime(get_begintime(nldas_2f_begin))
# nldasf_begintime = '01/02/1979 00:00:00'
nldas_2f = get_url2(nldas_1f)
nldasf_endtime = convert_datetime(get_endtime(nldas_2f))
nldasf_bounds = get_bounds(nldas_2f)

# GLDAS
gldas_2_begin = get_url2(gldas_1_begin)
gldas_begintime = convert_datetime(get_begintime(gldas_2_begin))
# gldas_begintime = '01/01/1998 00:00:00'
gldas_2 = get_url2(gldas_1)
gldas_endtime = convert_datetime(get_endtime(gldas_2))
gldas_bounds = get_bounds(gldas_2)

# GLDAS 2
gldas2_2_begin = get_url2(gldas2_1_begin)
gldas2_begintime = convert_datetime(get_begintime(gldas2_2_begin))
# gldas2_begintime = '01/01/2000 00:00:00'
gldas2_2 = get_url2(gldas2_1)
gldas2_endtime = convert_datetime(get_endtime(gldas2_2))
gldas2_bounds = get_bounds(gldas2_2)

# TRMM
trmm_2_begin = get_url2(trmm_1_begin)
trmm_begintime = convert_datetime(get_begintime(trmm_2_begin))
# trmm_begintime = '01/01/2000 00:00:00'
trmm_2 = get_url2(trmm_1)
trmm_endtime = convert_datetime(get_endtime(trmm_2))
trmm_bounds = get_bounds(trmm_2)

# GRACE
grace_2_begin = get_url2(grace_1_begin)
grace_begintime = convert_datetime(get_begintime(grace_2_begin))
# grace_begintime = '01/06/2003 00:00:00'
grace_2 = get_url2(grace_1)
grace_endtime = convert_datetime(get_endtime(grace_2))
grace_bounds = get_bounds(grace_2)

# Print results
columnheadings = "Model name | Begin time | End time | N , E , S , W bounds\n"
nldas_fences = "NLDAS|%s|%s|%s\n" % (nldas_begintime, nldas_endtime, nldas_bounds)
nldasf_fences = "NLDASF|%s|%s|%s\n" % (nldasf_begintime, nldasf_endtime, nldasf_bounds)
gldas_fences = "GLDAS|%s|%s|%s\n" % (gldas_begintime, gldas_endtime, gldas_bounds)
gldas2_fences = "GLDAS2|%s|%s|%s\n" % (gldas2_begintime, gldas2_endtime, gldas2_bounds)
trmm_fences = "TRMM|%s|%s|%s\n" % (trmm_begintime, trmm_endtime, trmm_bounds)
grace_fences = "GRACE|%s|%s|%s\n" % (grace_begintime, grace_endtime, grace_bounds)

# Alternate layout for organizing outputs
# begintimes = "NLDAS, %s\nNLDAS(Forcing): %s\nGLDAS: %s\nGLDAS2: %s\nTRMM: %s\nGRACE: %s\n" \
# 	% (nldas_begintime, nldasf_begintime, gldas_begintime, gldas2_begintime, trmm_begintime, grace_begintime)
#
# endtimes = "Current endtimes...\nNLDAS: %s\nNLDAS(Forcing): %s\nGLDAS: %s\nGLDAS2: %s\nTRMM: %s\nGRACE: %s\n" \
# 	% (nldas_endtime, nldasf_endtime, gldas_endtime, gldas2_endtime, trmm_endtime, grace_endtime)
#
# spatialbounds = "Current bounds...\nNLDAS: %s\nNLDAS(Forcing): %s\nGLDAS: %s\nGLDAS2: %s\nTRMM: %s\nGRACE: %s\n" \
# 	% (nldas_bounds, nldasf_bounds, gldas_bounds, gldas2_bounds, trmm_bounds, grace_bounds)

fencefile=inspect.getfile(inspect.currentframe()).replace('enddate_bounds.py','public/data/dates_and_spatial_range.txt')

with open(fencefile,mode='w+') as f:
	f.write(columnheadings)
	f.write(nldas_fences)
	f.write(nldasf_fences)
	f.write(gldas_fences)
	f.write(gldas2_fences)
	f.write(trmm_fences)
	f.write(grace_fences)


