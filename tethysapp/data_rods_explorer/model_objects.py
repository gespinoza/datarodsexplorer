from socket import gethostname
import inspect

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


def parse_model_database_from_file():
    db_file = inspect.getfile(inspect.currentframe()).replace('model_objects.py',
                                                              'public/data/model_config.txt')
    new_model_switch = False
    model_options = []
    var_dict = {}
    wms_vars = {}
    datarods_tsb = {}
    with open(db_file, mode='r') as f:
        f.readline()  # skip column headings line
        f.readline()
        for line in f.readlines():
            if line == '\n':
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


def set_model_options(model_options):
    global MODEL_OPTIONS
    MODEL_OPTIONS = model_options


def set_model_fences(model_fences):
    global MODEL_FENCES
    MODEL_FENCES = model_fences


def set_var_dict(var_dict):
    global VAR_DICT
    VAR_DICT = var_dict


def set_wms_vars(wms_vars):
    global WMS_VARS
    WMS_VARS = wms_vars


def set_datarods_tsb(datarods_tsb):
    global DATARODS_TSB
    DATARODS_TSB = datarods_tsb


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
