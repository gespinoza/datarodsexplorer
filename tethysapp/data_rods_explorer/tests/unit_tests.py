from django.shortcuts import render
from tethysapp.data_rods_explorer.model_objects import init_model, get_datarods_tsb, get_var_dict, get_model_fences
from datetime import datetime
import urllib2


def test_nasa_endpoints(request):
    init_model()
    model_fences = get_model_fences()
    datarods_tsb = get_datarods_tsb()
    var_dict = get_var_dict()

    counter = 0
    success = 0
    error = 0
    total_endpoints = 0
    failed_urls = []

    for model in model_fences:
        for _ in var_dict[model]:
            total_endpoints += 1

    for model in model_fences:
        nasa_url_template = datarods_tsb[model]
        start_date = datetime.strptime(model_fences[model]['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d') + 'T23'
        end_date = datetime.strptime(model_fences[model]['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d') + 'T00'
        extents = model_fences[model]['extents']
        y = float(extents['minY']) + ((float(extents['maxY']) - float(extents['minY'])) / 2)
        x = float(extents['minX']) + ((float(extents['maxX']) - float(extents['minX'])) / 2)
        lonlat = '%s%%2C%%20%s' % (x, y)
        for var_obj in var_dict[model]:
            counter += 1
            print "TESTING ENDPOINT %s of %s" % (counter, total_endpoints)
            var = var_obj['value']
            url = nasa_url_template.format(var, lonlat, start_date, end_date)
            try:
                nasa_file = urllib2.urlopen(url)
                if 'Date&Time' in nasa_file.read():
                    success += 1
                else:
                    error += 1
                    failed_urls.append(url)
            except Exception:
                error += 1
                failed_urls.append(url)

    results = '''
    TESTS COMPLETE!
    TOTAL ENDPOINTS TESTED: {0}
    TOTAL SUCCESSFUL: {1}
    TOTAL FAILS: {2}
    {3}{4}
    '''.format(counter, success, error,
               'FAILED ENDPOINTS: ' if len(failed_urls) > 0 else '',
               '\n'.join(failed_urls))

    print results
    context = {'results': '<br>'.join(results.split('\n'))}

    return render(request, 'data_rods_explorer/test-results.html', context)
