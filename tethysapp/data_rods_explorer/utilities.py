import os
from tethys_apps.base.persistent_store import get_persistent_store_engine as gpse
import inspect
from datetime import datetime, timedelta
from model_objects import MODEL_FENCES


def get_persistent_store_engine(persistent_store_name):
    """
    Returns an SQLAlchemy engine object for the persistent store name provided.
    """
    # Derive app name
    app_name = os.path.split(os.path.dirname(__file__))[1]

    # Get engine
    return gpse(app_name, persistent_store_name)


def get_fences():
    """
    Get date, time and spatial extent fences. Modelname will default to first one listed in input file.
    Begin dates will be actual model begin date + 1, and end dates will be actual model end date -1, to avoid chance
    of user selecting hours out of range for dates that are within range.
    """
    fencefile = inspect.getfile(inspect.currentframe()).replace('utilities.py',
                                                                'public/data/dates_and_spatial_range.txt')

    with open(fencefile, mode='r') as f:
        f.readline()  # skip column headings line
        for line in f.readlines():
            if not (line == '' or 'Model name' in line):      # end condition
                line = line.strip()
                linevals = line.split('|')
                start_date = (datetime.strptime(linevals[1].split(' ')[0], '%m/%d/%Y')+timedelta(days=1)).strftime('%m/%d/%Y')
                # begin_time = linevals[1].split(' ')[1]
                end_date = (datetime.strptime(linevals[2].split(' ')[0], '%m/%d/%Y')-timedelta(days=1)).strftime('%m/%d/%Y')
                # end_time = linevals[2].split(' ')[1]
                nbound = linevals[3].split(', ')[0]
                ebound = linevals[3].split(', ')[1]
                sbound = linevals[3].split(', ')[2]
                wbound = linevals[3].split(', ')[3]
                MODEL_FENCES[linevals[0]] = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'extents': {
                        'maxY': nbound,
                        'maxX': ebound,
                        'minY': sbound,
                        'minX': wbound
                    }
                }

    return MODEL_FENCES
