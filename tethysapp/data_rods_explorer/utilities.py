import os
from tethys_apps.base.persistent_store import get_persistent_store_engine as gpse
import inspect
from datetime import datetime, timedelta


def get_persistent_store_engine(persistent_store_name):
    """
    Returns an SQLAlchemy engine object for the persistent store name provided.
    """
    # Derive app name
    app_name = os.path.split(os.path.dirname(__file__))[1]

    # Get engine
    return gpse(app_name, persistent_store_name)


def parse_fences_from_file():
    """
    Get date, time and spatial extent fences. Modelname will default to first one listed in input file.
    Begin dates will be actual model begin date + 1, and end dates will be actual model end date -1, to avoid chance
    of user selecting hours out of range for dates that are within range.
    """
    fencefile = inspect.getfile(inspect.currentframe()).replace('utilities.py',
                                                                'public/data/dates_and_spatial_range.txt')

    model_fences = {}

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


def generate_datarods_urls_dict(asc2_urls):
    plot_urls = []
    waterml_urls = []

    for url in asc2_urls:
        plot_urls.append(url.replace('asc2', 'plot'))
        waterml_urls.append(url.replace('asc2', 'waterml'))

    return {
        'asc2': asc2_urls,
        'plot': plot_urls,
        'waterml': waterml_urls
    }


def parse_model_database_from_file():
    db_file = inspect.getfile(inspect.currentframe()).replace('utilities.py',
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
