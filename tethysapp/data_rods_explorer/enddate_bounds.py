import urllib
from sys import path
path.append('/usr/local/lib/python2.7/site-packages')  # This is so bs4 will be found
from bs4 import BeautifulSoup
import inspect


def extract_model_data_from_config_file():
    db_file = inspect.getfile(inspect.currentframe()).replace('enddate_bounds.py', 'public/data/model_config.txt')
    new_model_switch = False
    model_list = []

    with open(db_file, mode='r') as f:
        f.readline()  # skip column headings lines
        f.readline()
        for line in f.readlines():
            if line == '\n':
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
    fencefile = inspect.getfile(inspect.currentframe()).replace('enddate_bounds.py',
                                                                'public/data/dates_and_spatial_range.txt')

    # https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_FORA0125_H&version=002&page_size=1&sort_key=start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=NLDAS_NOAH0125_H&version=002&page_size=1&sort_key=start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_VIC10_3H&version=001&page_size=1&sort_key=start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GLDAS_NOAH025_3H&version=2.0&page_size=1&sort_key=start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=TRMM_3B42&version=7&page_size=1&sort_key=start_date
    # https://cmr.earthdata.nasa.gov/search/granules?short_name=GRACEDADM_CLSM025NA_7D&version=1.0&page_size=1&sort_key=start_date
    url_pattern = "https://cmr.earthdata.nasa.gov/search/granules?short_name={0}&version={1}&page_size=1&sort_key={2}"
    columnheadings = "Model name | Begin time | End time | N , E , S , W bounds\n"
    model_output_pattern = "{0}|{1}|{2}|{3}\n"

    with open(fencefile, mode='w+') as f:
        f.write(columnheadings)

        for model in model_list:
            middleman_url1 = url_pattern.format(model['short_name'], model['version'], 'start_date')
            print middleman_url1
            middleman_url2 = url_pattern.format(model['short_name'], model['version'], '-start_date')
            url1 = get_url2(middleman_url1)
            url2 = get_url2(middleman_url2)

            begin_time = convert_datetime(get_begintime(url1))
            end_time = convert_datetime(get_endtime(url2))
            bounds = get_bounds(url2)

            f.write(model_output_pattern.format(model['key'], begin_time, end_time, bounds))


# Find url2 from url1
def get_url2(url1):
    url_text1 = urllib.urlopen(url1)
    url_lines1 = url_text1.readlines()
    url2 = ""
    for i in range(len(url_lines1)):
        soup1 = BeautifulSoup(url_lines1[i], 'html.parser')
        if soup1.find("location") is not None:
            url2 = soup1.location.getText()
    return url2


# # Find begintime from url1
def get_begintime(url2):
    url_text2 = urllib.urlopen(url2)
    url_lines2 = url_text2.readlines()
    begintime = ""
    for j in range(len(url_lines2)):
        soup2 = BeautifulSoup(url_lines2[j], 'html.parser')
        if soup2.find("beginningdatetime") is not None:
            begintime = soup2.beginningdatetime.getText()
    return begintime


# Find endtime from url1
def get_endtime(url2):
    url_text2 = urllib.urlopen(url2)
    url_lines2 = url_text2.readlines()
    endtime = ""
    for j in range(len(url_lines2)):
        soup2 = BeautifulSoup(url_lines2[j], 'html.parser')
        if soup2.find("endingdatetime") is not None:
            endtime = soup2.endingdatetime.getText()
    return endtime


# Find bounding rectangle coordinates
def get_bounds(url2):
    url_text2 = urllib.urlopen(url2)
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
def convert_datetime(datetime):
    day = datetime[8:10]
    month = datetime[5:7]
    year = datetime[:4]
    hour = datetime[11:13]
    minute = datetime[14:16]
    second = datetime[17:19]
    return "%s/%s/%s %s:%s:%s" % (month, day, year, hour, minute, second)

models_list = extract_model_data_from_config_file()
write_fences_file(models_list)
