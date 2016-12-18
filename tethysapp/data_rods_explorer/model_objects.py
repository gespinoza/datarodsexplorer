from os import path
from datetime import datetime, timedelta
from requests import get
from tethys_sdk.services import get_spatial_dataset_engine
import os
from threading import Thread
from tempfile import NamedTemporaryFile
import urllib2
import zipfile
from math import copysign


WORKSPACE = 'data_rods_explorer'
DATARODS_PNG = ('http://giovanni.gsfc.nasa.gov/giovanni/daac-bin/wms_ag4?VERSION=1.1.1'
                '&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=512&HEIGHT=256'
                '&LAYERS=Time-Averaged.{5}'  # NLDAS_NOAH0125_M_002_soilm0_100cm
                '&STYLES=default&TRANSPARENT=TRUE&FORMAT=image/tiff'
                '&time={4}'  # 2008-01-01T00:00:00Z/2008-01-01T00:00:00Z
                '&bbox={0},{1},{2},{3}')  # -119,30,-107,36
MODEL_OPTIONS = []
MODEL_FENCES = {}
VAR_DICT = {}
WMS_VARS = {}
DATARODS_TSB = {}


class TiffLayerManager:
    loaded = False
    requested = False
    error = None
    async_thread = None
    zip_path = None
    store_name = None
    store_id = None
    plot_time = None
    model = None
    variable = None
    latlonbox = None
    time_st = None
    tiff_path = None
    prj_path = None
    tfw_path = None
    tiff_file = None
    geoserver_url = None

    def __init__(self):
        return

    def __new__(cls, *args, **kwargs):
        return

    @classmethod
    def reset(cls):
        cls.loaded = False
        cls.requested = False
        cls.error = None
        cls.async_thread = None
        cls.zip_path = None
        cls.store_name = None
        cls.store_id = None
        cls.plot_time = None
        cls.model = None
        cls.variable = None
        cls.latlonbox = None
        cls.time_st = None
        cls.tiff_path = None
        cls.prj_path = None
        cls.tfw_path = None
        cls.tiff_file = None
        cls.geoserver_url = None

    @classmethod
    def request_tiff_layer(cls, post_params):
        """
        This function returns the previously loaded map or the new map layer
        if the button on the page was clicked
        """
        if post_params.get('plotTime'):
            cls.plot_time = post_params['plotTime']

        if post_params.get('model'):
            cls.model = post_params['model']

        if post_params.get('variable'):
            cls.variable = post_params['variable']

        if cls.model and cls.variable and cls.plot_time:
            # Data rods parameters
            cls.latlonbox = [post_params['lonW'], post_params['latS'], post_params['lonE'], post_params['latN']]
            cls.time_st = cls.plot_time + ':00:00Z/' + cls.plot_time + ':00:30Z'
            cls.request_raster_zip()
        else:
            cls.error = 'Invalid parameters passed'

    @classmethod
    def request_raster_zip(cls):
        try:
            cls.requested = True
            # Files, paths, and store name & store id
            cls.tiff_file = NamedTemporaryFile(suffix=".tif", delete=False)
            cls.tiff_path = cls.tiff_file.name
            file_name = cls.tiff_file.name[:-4]
            cls.store_name = os.path.basename(file_name)
            cls.store_id = get_workspace() + ':' + cls.store_name
            cls.tfw_path = file_name + '.tfw'
            cls.prj_path = file_name + '.prj'
            cls.zip_path = file_name + '.zip'

            TiffLayerManager.async_thread = Thread(target=cls.download_raster_from_nasa,
                                                   args=(),
                                                   kwargs={})
            TiffLayerManager.async_thread.start()
        except Exception as e:
            print e.message
            cls.message = e.message

    @classmethod
    def download_raster_from_nasa(cls):
        try:
            minx, miny, maxx, maxy = cls.latlonbox
            # Create tiff file
            url_image = urllib2.urlopen(get_datarods_png().format(minx, miny, maxx, maxy,
                                                                  cls.time_st,
                                                                  get_wms_vars()[cls.model][cls.variable][0]))
            cls.tiff_file.write(url_image.read())
            cls.tiff_file.close()
            # Create prj file
            cls.create_prj_file()
            # Create tfw file
            cls.create_tfw_file()
            # Create zipfile
            cls.create_zip_file()

            cls.upload_layer_to_geoserver()
        except Exception as e:
            print e.message
            cls.message = e.message

    @classmethod
    def upload_layer_to_geoserver(cls):
        # Geoserver parameters
        geo_eng = get_spatial_dataset_engine(name='default')
        # Create raster in geoserver
        response = geo_eng.create_coverage_resource(store_id=cls.store_id,
                                                    coverage_file=cls.zip_path,
                                                    coverage_type='worldimage',
                                                    overwrite=True,
                                                    )
        if not response['success']:
            result = geo_eng.create_workspace(workspace_id=get_workspace(),
                                              uri='tethys_app-%s' % get_workspace())
            if result['success']:
                cls.upload_layer_to_geoserver()
        else:
            cls.geoserver_url = geo_eng.endpoint.replace('rest', 'wms')
            cls.loaded = True

    @classmethod
    def create_tfw_file(cls, h=256, w=512):
        minx, miny, maxx, maxy = cls.latlonbox
        hscx = copysign((float(maxx) - float(minx)) / w, 1)
        hscy = copysign((float(maxy) - float(miny)) / h, 1)
        tfw_file = open(cls.tfw_path, 'w')
        tfw_file.write('{0}\n'.format(hscx))
        tfw_file.write('0.0\n')
        tfw_file.write('0.0\n')
        tfw_file.write('{0}\n'.format(-hscy))
        tfw_file.write('{0}\n'.format(float(minx) - hscx / 2, float(minx)))
        tfw_file.write('{0}\n'.format(float(maxy) - hscy / 2, float(maxy)))
        tfw_file.write('')
        tfw_file.close()

    @classmethod
    def create_prj_file(cls):
        """
        This function creates the missing .prj file for the raster
        """
        prj_file = open(cls.prj_path, 'w')
        prj_file.write(('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
                        'SPHEROID["WGS_1984",6378137,298.257223563]],'
                        'PRIMEM["Greenwich",0],'
                        'UNIT["Degree",0.017453292519943295]]'
                        ))
        prj_file.close()

    @classmethod
    def create_zip_file(cls):
        """
        this function zips the tiff and prj files into
        """
        zip_file = zipfile.ZipFile(cls.zip_path, "w")
        zip_file.write(cls.tiff_path, arcname=os.path.basename(cls.tiff_path))
        zip_file.write(cls.tfw_path, arcname=os.path.basename(cls.tfw_path))
        zip_file.write(cls.prj_path, arcname=os.path.basename(cls.prj_path))
        zip_file.close()


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
