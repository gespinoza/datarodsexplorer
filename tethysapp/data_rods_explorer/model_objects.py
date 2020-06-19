from os import path
from datetime import datetime, timedelta
from requests import get
from tethys_sdk.services import get_spatial_dataset_engine
import os
from threading import Thread
from tempfile import NamedTemporaryFile
import urllib.request, urllib.error, urllib.parse
import zipfile
from math import copysign


WORKSPACE = 'data_rods_explorer'
DATARODS_PNG = ('http://giovanni.gsfc.nasa.gov/giovanni/daac-bin/wms_ag4?VERSION=1.1.1'
                '&SERVICE=WMS&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=512&HEIGHT=256'
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
    instances = {}

    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.loaded = False
        self.requested = False
        self.error = None
        self.message = None
        self.zip_path = None
        self.store_name = None
        self.store_id = None
        self.model = None
        self.variable = None
        self.latlonbox = None
        self.time_st = None
        self.tiff_path = None
        self.prj_path = None
        self.tfw_path = None
        self.tiff_file = None
        self.geoserver_url = None

    @classmethod
    def create_instance(cls, instance_id):
        cls.instances[instance_id] = TiffLayerManager(instance_id)
        return cls.get_instance(instance_id)

    @classmethod
    def get_instance(cls, instance_id):
        if instance_id not in cls.instances:
            return None

        return cls.instances[instance_id]

    def trash(self):
        try:
            del TiffLayerManager.instances[self.instance_id]
        except (NameError, KeyError):
            pass

    def request_tiff_layer(self, post_params):
        """
        This function returns the previously loaded map or the new map layer
        if the button on the page was clicked
        """
        Thread(target=self.request_tiff_layer_async,
               args=[post_params],
               kwargs={}).start()

    def request_tiff_layer_async(self, post_params):
        try:
            self.requested = True
            plot_time = post_params.get('plotTime', None)
            self.model = post_params.get('model', None)
            self.variable = post_params.get('variable', None)

            if self.model and self.variable and plot_time:
                # Data rods parameters
                self.latlonbox = [post_params['lonW'], post_params['latS'], post_params['lonE'], post_params['latN']]
                self.time_st = plot_time + ':00:00Z/' + plot_time + ':00:30Z'
            else:
                self.error = 'Invalid parameters passed'
                return

            # Files, paths, and store name & store id
            self.tiff_file = NamedTemporaryFile(suffix=".tif", delete=False)
            self.tiff_path = self.tiff_file.name
            file_name = self.tiff_file.name[:-4]
            self.store_name = os.path.basename(file_name)
            self.store_id = get_workspace() + ':' + self.store_name
            self.tfw_path = file_name + '.tfw'
            self.prj_path = file_name + '.prj'
            self.zip_path = file_name + '.zip'
            self.download_raster_from_nasa()
        except Exception as e:
            print(e.message)
            self.message = e.message

    def download_raster_from_nasa(self):
        try:
            minx, miny, maxx, maxy = self.latlonbox
            # Create tiff file
            url_image = urllib.request.urlopen(get_datarods_png().format(minx, miny, maxx, maxy,
                                                                  self.time_st,
                                                                  get_wms_vars()[self.model][self.variable][0]))
            self.tiff_file.write(url_image.read())
            self.tiff_file.close()
            # Create prj file
            self.create_prj_file()
            # Create tfw file
            self.create_tfw_file()
            # Create zipfile
            self.create_zip_file()

            self.upload_layer_to_geoserver()
        except Exception as e:
            print(str(e))
            self.message = str(e)

    def upload_layer_to_geoserver(self):
        # Geoserver parameters
        geo_eng = get_spatial_dataset_engine(name='default')
        # Create raster in geoserver
        response = geo_eng.create_coverage_resource(store_id=self.store_id,
                                                    coverage_file=self.zip_path,
                                                    coverage_type='worldimage',
                                                    overwrite=True,
                                                    )
        if not response['success']:
            result = geo_eng.create_workspace(workspace_id=get_workspace(),
                                              uri='tethys_app-%s' % get_workspace())
            if result['success']:
                self.upload_layer_to_geoserver()
        else:
            self.geoserver_url = geo_eng.endpoint.replace('rest', 'wms')
            self.loaded = True

    def create_tfw_file(self, h=256, w=512):
        minx, miny, maxx, maxy = self.latlonbox
        hscx = copysign((float(maxx) - float(minx)) / w, 1)
        hscy = copysign((float(maxy) - float(miny)) / h, 1)
        tfw_file = open(self.tfw_path, 'w')
        tfw_file.write('{0}\n'.format(hscx))
        tfw_file.write('0.0\n')
        tfw_file.write('0.0\n')
        tfw_file.write('{0}\n'.format(-hscy))
        tfw_file.write('{0}\n'.format(float(minx) - hscx / 2, float(minx)))
        tfw_file.write('{0}\n'.format(float(maxy) - hscy / 2, float(maxy)))
        tfw_file.write('')
        tfw_file.close()

    def create_prj_file(self):
        """
        This function creates the missing .prj file for the raster
        """
        prj_file = open(self.prj_path, 'w')
        prj_file.write(('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
                        'SPHEROID["WGS_1984",6378137,298.257223563]],'
                        'PRIMEM["Greenwich",0],'
                        'UNIT["Degree",0.017453292519943295]]'
                        ))
        prj_file.close()

    def create_zip_file(self):
        """
        this function zips the tiff and prj files into
        """
        zip_file = zipfile.ZipFile(self.zip_path, "w")
        zip_file.write(self.tiff_path, arcname=os.path.basename(self.tiff_path))
        zip_file.write(self.tfw_path, arcname=os.path.basename(self.tfw_path))
        zip_file.write(self.prj_path, arcname=os.path.basename(self.prj_path))
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
        line=line.decode()
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
