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

def get_fences(modelname=None):
    """
    Get date, time and spatial extent fences. Modelname will default to first one listed in input file.
    Begin dates will be actual model begin date + 1, and end dates will be actual model end date -1, to avoid chance
    of user selecting hours out of range for dates that are within range.
    """
    fencefile = inspect.getfile(inspect.currentframe()).replace('utilities.py',
                                                                'public/data/dates_and_spatial_range.txt')

    with open(fencefile, mode='r') as f:
        while True:
            line=f.readline()  # skip column headings line
            line=f.readline()
            if line == '':      # end condition
                break
            if not modelname:   # set default modelname to top of list in fencefile
                modelname = line.split('|')[0]
            if modelname in line:
                linevals = line.split('|')
                start_date = (datetime.strptime(linevals[1].split(' ')[0], '%m/%d/%Y')+timedelta(days=1)).strftime('%m/%d/%Y')
                # begin_time = linevals[1].split(' ')[1]
                end_date = (datetime.strptime(linevals[2].split(' ')[0], '%m/%d/%Y')-timedelta(days=1)).strftime('%m/%d/%Y')
                # end_time = linevals[2].split(' ')[1]
                nbound = linevals[3].split(', ')[0]
                ebound = linevals[3].split(', ')[1]
                sbound = linevals[3].split(', ')[2]
                wbound = linevals[3].split(', ')[3]
                break

    return modelname, start_date, end_date, nbound, ebound, sbound, wbound
