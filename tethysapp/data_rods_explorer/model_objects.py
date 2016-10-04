from socket import gethostname

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
