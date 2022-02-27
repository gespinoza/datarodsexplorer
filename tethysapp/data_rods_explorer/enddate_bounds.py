from urllib.request import urlopen
from os import path
from sys import path as syspath

syspath.append('/usr/local/lib/python2.7/site-packages')  # This is so bs4 and requests will be found #?
from requests import get
from bs4 import BeautifulSoup  # ?
from datetime import datetime, timedelta


def extract_model_data_from_config_file():
    # Attempt to parse model_config.txt from GitHub repo master branch
    db_file_url = ('https://raw.githubusercontent.com/CUAHSI-APPS/datarodsexplorer/master/tethysapp/'
                   'data_rods_explorer/public/data/model_config.txt')
    f = get(db_file_url)
    if f.status_code == 200:
        if f.encoding is None:
            f.encoding = 'utf-8'
        lines = f.iter_lines()
        next(lines)  # Skip first line
        next(lines)  # Skip second line
    else:
        # If the file cannot be parsed from GitHub, use the locally stored file instead
        db_file = path.join(path.dirname(path.realpath(__file__)), 'public/data/model_config.txt')
        with open(db_file, mode='r') as f:
            f.readline()  # Skip first line
            f.readline()  # Skip second line
            lines = f.readlines()

    new_model_switch = False
    model_list = []

    for line in lines:
        if type(line) == bytes:
            if f.encoding:
                line = str(line, f.encoding)
            else:
                line = str(line, 'utf-8')
        if line == '\n' or line == '':
            new_model_switch = True
            continue

        line = line.strip()
        linevals = line.split('|')
        if new_model_switch:
            model_vals = linevals[0].split('~')
            model_key = model_vals[1]
            model_short_name = model_vals[2]
            model_version = model_vals[3]
            model_list.append({
                'key': model_key,
                'short_name': model_short_name,
                'version': model_version
            })
            new_model_switch = False
    return model_list


def write_fences_file(model_list):
    fencefile = path.join(path.dirname(path.realpath(__file__)), 'public/data/dates_and_spatial_range.txt')
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_FORA0125_H&version=002&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_NOAH0125_H&version=002&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_NOAH025SUBP_3H&version=001&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_NOAH025_3H&version=2.0&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=TRMM_3B42&version=7&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=LPRM_AMSRE_D_SOILM3&version=002&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=LPRM_AMSRE_A_SOILM3&version=002&page_size=1&sort_key=-start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GRACEDADM_CLSM025NA_7D&version=1.0&page_size=1&sort_key=-start_date
    url_pattern = "https://cmr.earthdata.nasa.gov/search/granules?short_name={0}&version={1}&page_size=1&sort_key={2}"
    columnheadings = "Model name | Begin time | End time | N , E , S , W bounds\n"
    model_output_pattern = "{0}|{1}|{2}|{3}\n"

    with open(fencefile, mode='w+') as f:
        f.write(columnheadings)

        for model in model_list:
            middleman_url1 = url_pattern.format(model['short_name'], model['version'], 'start_date')
            print(middleman_url1)
            middleman_url2 = url_pattern.format(model['short_name'], model['version'], '-start_date')
            url1 = get_url2(middleman_url1)
            url2 = get_url2(middleman_url2)
            try:
                begin_time = convert_datetime(get_begintime(url1))
                end_time = convert_datetime(get_endtime(url2))
                bounds = get_bounds(url2)
            except:
                print(model["key"] + " failed to get dates and spatial range.")
                f.write(model_output_pattern.format(model['key'], "", "", ""))
                continue

            if model['key'] == 'GLDAS':
                end_date = get_endtime(url2).split('T')[0]
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                start_date = (end_date_obj - timedelta(days=5)).strftime('%Y-%m-%d')

                test_url = 'http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?' \
                           'variable=GLDAS:GLDAS_NOAH025_3H.001:Evap&startDate={0}T00&endDate={1}T00&' \
                           'location=GEOM:POINT(10.0%2C%200.0)&type=asc2'.format(start_date, end_date)
                nasa_file = urlopen(test_url)

                for line in nasa_file.readlines():
                    line = line.strip()
                    if 'begin_time' in line:
                        begin_time = datetime.strptime(line.split('=')[1], '%Y/%m/%d/%H').strftime('%m/%d/%Y %H:00:00')
                        continue
                    if 'end_time' in line:
                        end_time = datetime.strptime(line.split('=')[1], '%Y/%m/%d/%H').strftime('%m/%d/%Y %H:00:00')
                        break
            if begin_time == "":
                begin_time = '04/01/2002 00:00:00'
            f.write(model_output_pattern.format(model['key'], begin_time, end_time, bounds))


# Find url2 from url1
def get_url2(url1):
    url_text1 = urlopen(url1)
    url_lines1 = url_text1.readlines()
    url2 = ""
    for i in range(len(url_lines1)):
        soup1 = BeautifulSoup(url_lines1[i], 'html.parser')
        if soup1.find("location") is not None:
            url2 = soup1.location.getText()
    return url2


# # Find begintime from url1
def get_begintime(url2):
    url_text2 = urlopen(url2)
    url_lines2 = url_text2.readlines()
    begintime = ""
    for j in range(len(url_lines2)):
        soup2 = BeautifulSoup(url_lines2[j], 'html.parser')
        if soup2.find("beginningdatetime") is not None:
            begintime = soup2.beginningdatetime.getText()
    return begintime


# Find endtime from url1
def get_endtime(url2):
    url_text2 = urlopen(url2)
    url_lines2 = url_text2.readlines()
    endtime = ""
    for j in range(len(url_lines2)):
        soup2 = BeautifulSoup(url_lines2[j], 'html.parser')
        if soup2.find("endingdatetime") is not None:
            endtime = soup2.endingdatetime.getText()
    return endtime


# Find bounding rectangle coordinates
def get_bounds(url2):
    url_text2 = urlopen(url2)
    url_lines2 = url_text2.readlines()
    nbound = None
    ebound = None
    sbound = None
    wbound = None

    for k in range(len(url_lines2)):
        soup2 = BeautifulSoup(url_lines2[k], 'html.parser')
        if soup2.find("northboundingcoordinate"):
            nbound = soup2.northboundingcoordinate.getText()
        if soup2.find("eastboundingcoordinate"):
            ebound = soup2.eastboundingcoordinate.getText()
        if soup2.find("southboundingcoordinate"):
            sbound = soup2.southboundingcoordinate.getText()
        if soup2.find("westboundingcoordinate"):
            wbound = soup2.westboundingcoordinate.getText()
    bounds = "%s, %s, %s, %s" % (nbound, ebound, sbound, wbound)
    return bounds


# Convert datetime to mm/dd/yyyy
def convert_datetime(date_time):
    day = date_time[8:10]
    month = date_time[5:7]
    year = date_time[:4]
    hour = date_time[11:13]
    minute = date_time[14:16]
    second = date_time[17:19]
    return "%s/%s/%s %s:%s:%s" % (month, day, year, hour, minute, second)


models_list = extract_model_data_from_config_file()
write_fences_file(models_list)
