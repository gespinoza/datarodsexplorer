import inspect
from datetime import datetime, timedelta


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
