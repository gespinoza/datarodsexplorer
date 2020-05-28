from django.shortcuts import render
from tethysapp.data_rods_explorer.model_objects import init_model, get_datarods_tsb, get_var_dict, get_model_fences
from datetime import datetime, timedelta
from urllib2 import urlopen
from django.http import JsonResponse
from json import dumps
from threading import Thread


class TestManager:
    total_endpoints = 0
    counter = 0
    failed_urls = []
    results = None
    complete = False

    def __new__(cls, *args, **kwargs):
        return

    def __init__(self):
        return

    @classmethod
    def run_tests(cls, full=False):
        start = datetime.now()
        init_model()
        model_fences = get_model_fences()
        datarods_tsb = get_datarods_tsb()
        var_dict = get_var_dict()

        cls.total_endpoints = 0
        cls.counter = 0
        cls.failed_urls = []
        cls.results = None
        cls.complete = False
        success = 0
        error = 0

        for model in model_fences:
            for _ in var_dict[model]:
                cls.total_endpoints += 1

        for model in model_fences:
            nasa_url_template = datarods_tsb[model]

            # If testing range of all available dates
            if full:
                start_date = datetime.strptime(model_fences[model]['start_date'], '%m/%d/%Y').strftime(
                    '%Y-%m-%d') + 'T23'
                end_date = datetime.strptime(model_fences[model]['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d') + 'T00'
            else:
                # If testing latest week (Default)
                end_date_obj = datetime.strptime(model_fences[model]['end_date'], '%m/%d/%Y')
                end_date = end_date_obj.strftime('%Y-%m-%d') + 'T00'
                start_date = (end_date_obj - timedelta(days=7)).strftime('%Y-%m-%d') + 'T00'

            extents = model_fences[model]['extents']
            y = float(extents['minY']) + ((float(extents['maxY']) - float(extents['minY'])) / 2)
            x = float(extents['minX']) + ((float(extents['maxX']) - float(extents['minX'])) / 2)
            lonlat = '%s%%2C%%20%s' % (x, y)
            for var_obj in var_dict[model]:
                cls.counter += 1
                var = var_obj['value']
                url = nasa_url_template.format(var, lonlat, start_date, end_date)
                try:
                    nasa_file = urlopen(url)
                    if 'Date&Time' in nasa_file.read():
                        success += 1
                    else:
                        error += 1
                        cls.failed_urls.append(url)
                except Exception:
                    error += 1
                    cls.failed_urls.append(url)

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
            '''.format(start, end, elapsed, cls.counter, success, error)

        cls.results = '<br>'.join(results_text.split('\n'))

        cls.complete = True


def test_nasa_endpoints(request):
    if request.is_ajax() and request.method == 'GET':
        if TestManager.complete:
            context = {
                'results': TestManager.results,
                'failed_urls': dumps(TestManager.failed_urls)
            }
            return JsonResponse(context)
        else:
            context = {
                'counter': TestManager.counter,
                'total_endpoints': TestManager.total_endpoints
            }
            return JsonResponse(context)
    else:
        full = False
        if request.GET.get('full') and request.GET['full'] == 'true':
            full = True
        async_thread = Thread(target=TestManager.run_tests,
                              args=[full],
                              kwargs={})
        async_thread.start()

        return render(request, 'data_rods_explorer/test-results.html', {})
