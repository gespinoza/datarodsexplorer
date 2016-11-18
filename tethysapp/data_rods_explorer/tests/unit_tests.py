from django.shortcuts import render
from tethysapp.data_rods_explorer.model_objects import init_model, get_datarods_tsb, get_var_dict, get_model_fences
from datetime import datetime, timedelta
import urllib2


def test_nasa_endpoints(request):
    start = datetime.now()
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
        # Use if testing range of all available dates
        # start_date = datetime.strptime(model_fences[model]['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d') + 'T23'
        # end_date = datetime.strptime(model_fences[model]['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d') + 'T00'
        # Use if specifying a smaller subset of available dates from latest date backwards
        end_date_obj = datetime.strptime(model_fences[model]['end_date'], '%m/%d/%Y')
        end_date = end_date_obj.strftime('%Y-%m-%d') + 'T00'
        start_date = (end_date_obj - timedelta(days=7)).strftime('%Y-%m-%d') + 'T00'
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

    end = datetime.now()
    elapsed = end - start

    results_text = '''
    TESTS COMPLETE!

    SUMMARY:

        START TIME: {0}
        END TIME: {1}
        ELAPSED TIME: {2}
        TOTAL ENDPOINTS TESTED: {3}
        TOTAL SUCCESSFUL: {4}
        TOTAL FAILS: {5}
    '''.format(start, end, elapsed, counter, success, error)

    if failed_urls:
        console_results = results_text + '\n\tFAILED ENDPOINTS:\n\t' + '\n\t'.join(failed_urls)
    else:
        console_results = results_text

    print console_results

    context = {
        'results_text': '<br>'.join(results_text.split('\n')),
        'failed_urls': failed_urls
    }

    return render(request, 'data_rods_explorer/test-results.html', context)
