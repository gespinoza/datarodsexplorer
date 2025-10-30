from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from requests import get
from tethys_sdk.gizmos import SelectInput, Button, TimeSeries, MapView
from tethys_sdk.routing import controller
from .model_objects import get_wms_vars, get_datarods_png, get_datarods_tsb, \
    get_model_fences, get_model_options, get_var_dict, init_model, TiffLayerManager
from .utilities import create_map, create_select_model, create_plot_ctrls, create_map_date_ctrls, \
    create_years_list, format_csv_data, get_data_rod_plot, get_data_rod_plot2, get_data_rod_years, get_data_from_nasa_server
from json import dumps
import io
import zipfile
from tethys_sdk.routing import controller


@controller(name='home', url='data-rods-explorer')
def home(request):
    """
    Controller for the app 'home' page.
    """

    init_model()

    model = get_model_options()[0][1]

    select_model = create_select_model(model)
    select_date, select_hour = create_map_date_ctrls(model)

    # Load map
    map_view_options = create_map()

    start_date1, end_date1, plot_button1 = create_plot_ctrls(model, 'plot')
    start_date2, end_date2, plot_button2 = create_plot_ctrls(model, 'plot2')
    select_model2 = SelectInput(display_text='',
                                name='model2',
                                multiple=False,
                                original=True,
                                options=get_model_options(),
                                attributes="onchange=oc_model2();",
                                classes="w-100 mb-3 form-control"
                                )

    years_list = create_years_list(1979)
    select_years = SelectInput(display_text='',
                               name='years',
                               multiple=True,
                               original=False,
                               options=years_list,
                               attributes="onchange=oc_years();"
                               
                               )

    plot_button3 = Button(display_text='Plot',
                          name='years',
                          style='',
                          icon='',
                          href='',
                          submit=False,
                          disabled=False,
                          attributes='onclick=createPlot(this.name);',
                          classes='btn-plot mb-3')

    # Context variables
    context = {
        'select_model': select_model,
        'map_view_options': map_view_options,
        'select_date': select_date,
        'select_hour': select_hour,
        'MODEL_FENCES': dumps(get_model_fences()),
        'VAR_DICT': dumps(get_var_dict()),
        'DATARODS_PNG': dumps(get_datarods_png()),
        'DATARODS_TSB': dumps(get_datarods_tsb()),
        'WMS_VARS': dumps(get_wms_vars()),
        'start_date1': start_date1,
        'end_date1': end_date1,
        'plot_button1': plot_button1,
        'start_date2': start_date2,
        'end_date2': end_date2,
        'plot_button2': plot_button2,
        'select_model2': select_model2,
        'plot_button3': plot_button3,
        'select_years': select_years
    }

    return render(request, 'data_rods_explorer/app_base_dre.html', context)

@controller(name='map', url='data-rods-explorer/request-map-layer')
def request_map_layer(request):
    context = {
        'success': False
    }
    if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.method == 'POST':
        post_params = request.POST
        instance_id = post_params['instance_id']
        tif_layer_manager = TiffLayerManager.get_instance(instance_id)

        if tif_layer_manager:
            if tif_layer_manager.requested:
                if tif_layer_manager.loaded:
                    context = {
                        'success': True,
                        'load_layer': tif_layer_manager.store_id,
                        'geoserver_url': tif_layer_manager.geoserver_url
                    }
                    tif_layer_manager.trash()
                elif tif_layer_manager.error:
                    print('request map layer error')
                    context['error'] = tif_layer_manager.error
                    tif_layer_manager.trash()
        else:
            # If 'Display map' is clicked, load layers
            tif_layer_manager = TiffLayerManager.create_instance(instance_id)
            tif_layer_manager.request_tiff_layer(post_params)
            if tif_layer_manager.error is not None:
                context['success'] = False
                context['error'] = tif_layer_manager.error
            else:
                context['success'] = True
    return JsonResponse(context)

@controller(name='plot', url='data-rods-explorer/plot')
def plot(request):
    """
    Controller for the plot page.
    """
    post = request.POST
    context = {}

    # Plot
    if post and post['pointLonLat'] != '-9999':
        try:
            varname = get_wms_vars()[post['model']][post['map_variable']][1]
            varunit = get_wms_vars()[post['model']][post['map_variable']][2]
            point_lon_lat = post['pointLonLat']
            datarod_ts = get_data_rod_plot(post, point_lon_lat)
            timeseries_plot = TimeSeries(
                height='250px',
                width='100%',
                engine='highcharts',
                title=False,
                y_axis_title=varname,
                y_axis_units=varunit,
                series=[{
                    'name': '%s (Lon,Lat)' % point_lon_lat,
                    'data': datarod_ts
                }]
            )
            context = {
                'timeseries_plot': timeseries_plot,
                'plot_type': 'plot'
            }
        except Exception as e:
            print(str(e))
            if 'ERROR 999' in str(e):
                context = {
                    'error': str(e)
                }
            else:
                context = {
                    'error': 'An unknown error occurred.'
                }

    return render(request, 'data_rods_explorer/plot.html', context)

@controller(name='plot2', url='data-rods-explorer/plot2')
def plot2(request):
    """
    Controller for the plot2 page.
    """
    post = request.POST

    # Plot
    if post and post['pointLonLat'] != '-9999':
        point_lon_lat = post['pointLonLat']
        datarod_ts = get_data_rod_plot2(post, point_lon_lat)
        timeseries_plot = {'y1_axis_units': get_wms_vars()[post['model']][post['map_variable']][2],
                           'y2_axis_units': get_wms_vars()[post['model2']][post['map_variable2']][2],
                           'series': datarod_ts}

        context = {
            'timeseries_plot': timeseries_plot,
            'plot_type': 'plot2',
        }

        return render(request, 'data_rods_explorer/plot.html', context)

@controller(name='years', url='data-rods-explorer/years')
def years(request):
    """
    Controller for the 'years' page.
    """
    post = request.POST

    # Plot
    if post and post['pointLonLat'] != '-9999':
        varname = get_wms_vars()[post['model']][post['map_variable']][1]
        varunit = get_wms_vars()[post['model']][post['map_variable']][2]
        point_lon_lat = post['pointLonLat']
        datarod_ts = get_data_rod_years(post, point_lon_lat)
        timeseries_plot = TimeSeries(
            height='250px',
            width='100%',
            engine='highcharts',
            title=False,
            y_axis_title=varname,
            y_axis_units=varunit,
            series=datarod_ts
        )

        context = {
            'timeseries_plot': timeseries_plot,
            'plot_type': 'years'
        }

        return render(request, 'data_rods_explorer/plot.html', context)

@controller(name='proxy_download', url='data-rods-explorer/raw-data/{output_type}')
def get_raw_data(request, output_type):
    """
    Controller to get raw data from NASA server as a download or to view in browser.
    """
    get_params = request.GET
    try:
        if "years" in get_params:
            year_data = {}
            request_params = {"plot_variable": get_params['plot_variable'],
                              "lon": get_params['lon'],
                              "lat": get_params['lat'],
                              }
            if 'overlap_years' in get_params:
                overlap_years = True if 'true' in get_params['overlap_years'] else False
            else:
                overlap_years = False

            plot_variable = get_params['plot_variable']

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for year in get_params['years'].split(','):
                    if "-" in year:
                        year_range = year.split("-")
                        for yyyy in range(int(year_range[0]), int(year_range[1]) + 1):
                            start_date = f"{yyyy}-01-01T00"
                            end_date = f"{yyyy}-12-31T23"
                            request_params["start_date"] = start_date
                            request_params["end_date"] = end_date
                            data = get_data_from_nasa_server(request_params, overlap_years=overlap_years, full_output=True)
                            if output_type == "csv":
                                file_name = f"{plot_variable}_{yyyy}_data.csv"
                                file_contents = data["content"]
                                zipf.writestr(file_name, file_contents)
                            elif output_type == "txt":
                                file_name = f"{plot_variable}_{yyyy}_data.txt"
                                file_contents = format_csv_data(data["content"])
                                zipf.writestr(file_name, file_contents)
                    else:
                        start_date = f"{year}-01-01T00"
                        end_date = f"{year}-12-31T23"
                        request_params["start_date"] = start_date
                        request_params["end_date"] = end_date
                        data = get_data_from_nasa_server(request_params, overlap_years=overlap_years, full_output=True)

                        if output_type == "csv":
                            file_name = f"{plot_variable}_{year}_data.csv"
                            file_contents = data["content"]
                            zipf.writestr(file_name, file_contents)
                        elif output_type == "txt":
                            file_name = f"{plot_variable}_{year}_data.txt"
                            file_contents = format_csv_data(data["content"])
                            zipf.writestr(file_name, file_contents)
                        elif output_type == "browser":
                            data = format_csv_data(data["content"])
                            year_data[year] = data

            if output_type == "browser":
                context = {"type": "years",
                           "variable": get_params['plot_variable'],
                           "data": year_data}
                return render(request, 'data_rods_explorer/view_data.html', context)
            
            zip_buffer.seek(0)

            response = HttpResponse(zip_buffer, content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename="data_rods_data.zip"'
            return response            

        elif "plot_variable2" in get_params:
            start_date = get_params['startDate']
            end_date = get_params['endDate']
            request_params = {"lon": get_params['lon'],
                              "lat": get_params['lat'],
                              "start_date": start_date,
                              "end_date": end_date,
                            }
            request_params["plot_variable"] = get_params['plot_variable']
            data_1 = get_data_from_nasa_server(request_params, full_output=True)

            request_params["plot_variable"] = get_params['plot_variable2']
            data_2 = get_data_from_nasa_server(request_params, full_output=True)

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                if output_type == "csv":
                    filename_1 = f"{get_params['plot_variable']}_{start_date}_to_{end_date}.csv"
                    filename_2 = f"{get_params['plot_variable2']}_{start_date}_to_{end_date}.csv"
                    zipf.writestr(filename_1, data_1["content"])
                    zipf.writestr(filename_2, data_2["content"])
                
                elif output_type == "txt":
                    filename_1 = f"{get_params['plot_variable']}_{start_date}_to_{end_date}.txt"
                    filename_2 = f"{get_params['plot_variable2']}_{start_date}_to_{end_date}.txt"
                    file_1_contents = format_csv_data(data_1["content"])
                    file_2_contents = format_csv_data(data_2["content"])
                    zipf.writestr(filename_1, file_1_contents)
                    zipf.writestr(filename_2, file_2_contents)

                elif output_type == "browser":
                    data1 = format_csv_data(data_1["content"])
                    data2 = format_csv_data(data_2["content"])
                    context = {"type": "dual",
                               "variable_1": get_params['plot_variable'],
                               "variable_2": get_params['plot_variable2'], 
                               "data1": data1,
                               "data2": data2}
                    return render(request, 'data_rods_explorer/view_data.html', context)

            zip_buffer.seek(0)

            response = HttpResponse(zip_buffer, content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename="data_rods_data.zip"'
            return response
        
        else:
            start_date = get_params['startDate']
            end_date = get_params['endDate']
            request_params = {"plot_variable": get_params['plot_variable'],
                              "lon": get_params['lon'],
                              "lat": get_params['lat'],
                              "start_date": start_date,
                              "end_date": end_date,
                            }
            data = get_data_from_nasa_server(request_params, full_output=True)
            if output_type == "csv":
                filename = f"{get_params['plot_variable']}_{start_date}_to_{end_date}.csv"
                contents = data["content"]
            elif output_type == "txt":
                filename = f"{get_params['plot_variable']}_{start_date}_to_{end_date}.txt"
                contents = format_csv_data(data["content"])

            elif output_type == "browser":
                data = format_csv_data(data["content"])
                context = {"type": "single",
                           "variable": get_params['plot_variable'],
                           "data": data}
                return render(request, 'data_rods_explorer/view_data.html', context)

            response = HttpResponse(contents, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    except Exception as e:
        print(str(e))
        return HttpResponse(f"There was an error processing your request.", status=500)
    
'''
def upload_to_hs(request):
    if request.is_ajax() and request.method == 'GET':
        res_id = None
        params = request.GET
        res_type = params.get('res_type', None)
        res_title = params.get('res_title', None)
        res_abstract = params.get('res_abstract', None)
        res_keywords = params.get('res_keywords', None)
        rods_endpoints = params.get('rods_endpoints', None)
        plot_type = params.get('plot_type', None)

        if rods_endpoints:
            rods_endpoints = literal_eval(str(rods_endpoints))

        try:
            hs = get_oauth_hs(request)
        except:
            # Uncomment if testing locally
            # from hs_restclient import HydroShare, HydroShareAuthBasic
            # hs = HydroShare(auth=HydroShareAuthBasic(username='test', password='test'))
            return JsonResponse({
                'success': False,
                'message': 'You must be logged into the app through HydroShare to access this feature.'
            })

        num_endpoints = len(rods_endpoints)

        for i, url in enumerate(rods_endpoints):
            with TemporaryFile() as f:
                r = get(str(url))

                for chunk in r.iter_content(chunk_size=2048):
                    f.write(chunk)

                f.seek(0)
                params = parse_qs(urlsplit(url).query)
                lonlat = params['location'][0][11:-1].split(', ')
                variable_full = params['variable'][0]
                variable_short = variable_full[variable_full.find(':')+1:]
                variable = variable_short.replace('.', '_').replace(':', '_')
                fname_base = '{variable}_{lon}E{lat}N'.format(variable=variable,
                                                              lon=lonlat[0],
                                                              lat=lonlat[1])
                fname_ext = 'nc' if 'netcdf' in str(url) else 'txt'

                if plot_type == 'years':
                    year = params['endDate'][0][:4]
                    filename = '{base}_{year}.{ext}'.format(base=fname_base, year=year, ext=fname_ext)
                else:
                    filename = '{base}.{ext}'.format(base=fname_base, ext=fname_ext)

                # Netcdf resources can only have one file, so if there are more than one, create a GenericResource
                if res_type == 'NetcdfResource' and num_endpoints > 1:
                    res_type = 'GenericResource'

                # Resource should only be created the first time, then added to all subsequent times
                if i == 0:
                    res_id = hs.createResource(resource_type=str(res_type),
                                               title=str(res_title),
                                               resource_filename=filename,
                                               resource_file=f,
                                               abstract=str(res_abstract) if res_abstract else None,
                                               keywords=str(res_keywords).split(',') if res_keywords else None)
                else:
                    counter = 0
                    failed = True
                    while failed:
                        if counter == 15:
                            raise Exception
                        try:
                            hs.addResourceFile(res_id, resource_filename=filename, resource_file=f)
                            failed = False
                        except hs.HydroShareHTTPException as e:
                            if 'with method POST and params None' in str(e):
                                failed = True
                                counter += 1
                            else:
                                raise e

        return JsonResponse({
            'success': True,
            'res_id': res_id
        })
'''
