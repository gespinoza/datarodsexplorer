from socket import gethostname
from os import path
from datetime import datetime, timedelta
from requests import get


if 'apps.hydroshare' in gethostname():
    GEOSERVER_URL = 'http://apps.hydroshare.org:8181/geoserver/wms'
elif 'appsdev.hydroshare' in gethostname():
    GEOSERVER_URL = 'http://appsdev.hydroshare.org:8181/geoserver/wms'
else:
    GEOSERVER_URL = 'http://127.0.0.1:8181/geoserver/wms'

WORKSPACE = 'data_rods_explorer'
MODEL_OPTIONS = []
MODEL_FENCES = {}
VAR_DICT = {}
WMS_VARS = {}
DATARODS_TSB = {}
DATARODS_PNG = ('http://giovanni.gsfc.nasa.gov/giovanni/daac-bin/wms_ag4?VERSION=1.1.1'
                '&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=512&HEIGHT=256'
                '&LAYERS=Time-Averaged.{5}'  # NLDAS_NOAH0125_M_002_soilm0_100cm
                '&STYLES=default&TRANSPARENT=TRUE&FORMAT=image/tiff'
                '&time={4}'  # 2008-01-01T00:00:00Z/2008-01-01T00:00:00Z
                '&bbox={0},{1},{2},{3}')  # -119,30,-107,36


def init_model():
    global MODEL_OPTIONS, VAR_DICT, WMS_VARS, DATARODS_TSB, MODEL_FENCES

    MODEL_OPTIONS, VAR_DICT, WMS_VARS, DATARODS_TSB = parse_model_database_from_file()
    MODEL_FENCES = parse_fences_from_file()


def get_model_options():
    global MODEL_OPTIONS
    return MODEL_OPTIONS


def get_model_fences():
    global MODEL_FENCES
    return MODEL_FENCES


def get_var_dict():
    global VAR_DICT
    return VAR_DICT


def get_wms_vars():
    global WMS_VARS
    return WMS_VARS


def get_datarods_tsb():
    global DATARODS_TSB
    return DATARODS_TSB


def get_workspace():
    global WORKSPACE
    return WORKSPACE


def get_geoserver_url():
    global GEOSERVER_URL
    return GEOSERVER_URL


def get_datarods_png():
    global DATARODS_PNG
    return DATARODS_PNG


def parse_fences_from_file():
    """
    Get date, time and spatial extent fences. Modelname will default to first one listed in input file.
    Begin dates will be actual model begin date + 1, and end dates will be actual model end date -1, to avoid chance
    of user selecting hours out of range for dates that are within range.
    """
    model_fences = {}

    fencefile = path.join(path.dirname(path.realpath(__file__)), 'public/data/dates_and_spatial_range.txt')

    with open(fencefile, mode='r') as f:
        f.readline()  # skip column headings line
        for line in f.readlines():
            if not (line == '' or 'Model name' in line):      # end condition
                line = line.strip()
                linevals = line.split('|')
                start_date = (datetime.strptime(linevals[1].split(' ')[0], '%m/%d/%Y') + timedelta(days=1)) \
                    .strftime('%m/%d/%Y')
                # begin_time = linevals[1].split(' ')[1]
                end_date = (datetime.strptime(linevals[2].split(' ')[0], '%m/%d/%Y') - timedelta(days=1)) \
                    .strftime('%m/%d/%Y')
                # end_time = linevals[2].split(' ')[1]
                nbound = linevals[3].split(', ')[0]
                ebound = linevals[3].split(', ')[1]
                sbound = linevals[3].split(', ')[2]
                wbound = linevals[3].split(', ')[3]
                model_fences[linevals[0]] = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'extents': {
                        'maxY': nbound,
                        'maxX': ebound,
                        'minY': sbound,
                        'minX': wbound
                    }
                }

    return model_fences


def parse_model_database_from_file():
    # Attempt to parse model_config.txt from GitHub repo master branch
    db_file_url = ('https://raw.githubusercontent.com/gespinoza/datarodsexplorer/master/tethysapp/'
                   'data_rods_explorer/public/data/model_config.txt')
    f = get(db_file_url)
    if f.status_code == 200:
        if f.encoding is None:
            f.encoding = 'utf-8'
        lines = f.iter_lines(decode_unicode=True)
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
    model_options = []
    var_dict = {}
    wms_vars = {}
    datarods_tsb = {}

    for line in lines:
        if line == '\n' or line == '':
            new_model_switch = True
            continue
        line = line.strip()
        linevals = line.split('|')
        if new_model_switch:
            model_vals = linevals[0].split('~')
            model_name = model_vals[0]
            model_key = model_vals[1]
            datarods_tsb[model_key] = model_vals[4]
            model_options.append((model_name, model_key))
            new_model_switch = False
            continue
        else:
            model_key = linevals[0]

            if model_key not in wms_vars:
                wms_vars[model_key] = {}

            wms_vars[model_key][linevals[1]] = [linevals[2], linevals[3], linevals[4]]

            if model_key not in var_dict:
                var_dict[model_key] = []

            var_dict[model_key].append({
                "text": "%s %s" % (linevals[3], linevals[4]),
                "value": linevals[1],
                "layerName": linevals[5]
            })

    return model_options, var_dict, wms_vars, datarods_tsb
