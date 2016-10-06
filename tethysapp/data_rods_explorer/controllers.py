# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from tethys_sdk.gizmos import SelectInput, MapView, MVView, DatePicker, Button, MVLayer, TimeSeries
from tethys_sdk.services import get_spatial_dataset_engine
import os
from datetime import datetime
import zipfile
from tempfile import NamedTemporaryFile
import urllib2
from math import copysign
from utilities import parse_fences_from_file, generate_datarods_urls_dict, parse_model_database_from_file
from model_objects import *
from json import dumps
from dateutil import parser


def home(request):
    """
    Controller for the app 'home' page.
    """
    model_options, var_dict, wms_vars, datarods_tsb = parse_model_database_from_file()
    set_model_options(model_options)
    set_var_dict(var_dict)
    set_wms_vars(wms_vars)
    set_datarods_tsb(datarods_tsb)
    set_model_fences(parse_fences_from_file())

    get = request.GET
    post = request.POST
    context = initialize_model_map_context(get, post)

    context['messages'] = [{
        'category': 'info',
        'text': 'Click on the map to define data query location.'
    }]
    context['VAR_DICT'] = dumps(get_var_dict())

    return render(request, 'data_rods_explorer/app_base_dre.html', context)


def map_view(request):
    get = request.GET
    post = request.POST
    # If 'Display map' is clicked, load layers
    map_layers = load_tiff_ly(post, get)
    if map_layers:
        load_layer = map_layers[0]['options']['params']['LAYERS']
    else:
        load_layer = ''

    context = {
        'load_layer': load_layer,
        'geoserver_url': get_geoserver_url()
    }

    return JsonResponse(context)


def plot(request):
    """
    Controller for the plot page.
    """
    get = request.GET
    post = request.POST

    # Plot
    if (post and post['prevPlot'] == 'yes') or (post and post['pointLonLat'] != '-9999'):
        try:
            varname = get_wms_vars()[post['model']][post['variable']][1]
            varunit = get_wms_vars()[post['model']][post['variable']][2]
            point_lon_lat = post['pointLonLat']
            datarod_ts, datarods_urls_dict = get_data_rod_plot(post, point_lon_lat)
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
                'datarods_urls_dict': datarods_urls_dict
            }
        except Exception as e:
            if e.error == 999:
                context = {
                    'error': e.message
                }

        return render(request, 'data_rods_explorer/plot.html', context)

    else:
        model = str(get['model'].upper())
        start_date, end_date, plot_button = plot_ctrls(model, 'plot')
        context = {
            'start_date': start_date,
            'end_date': end_date,
            'plot_button': plot_button
        }

    return render(request, 'data_rods_explorer/nav_plot.html', context)


def plot2(request):
    """
    Controller for the plot2 page.
    """
    post = request.POST
    get = request.GET

    # Plot
    if (post and post['prevPlot'] == 'yes') or (post and post['pointLonLat'] != '-9999'):
        point_lon_lat = post['pointLonLat']
        datarod_ts, datarods_urls_dict = get_data_rod_plot2(post, point_lon_lat)
        timeseries_plot = {'y1_axis_units': get_wms_vars()[post['model']][post['variable']][2],
                           'y2_axis_units': get_wms_vars()[post['model2']][post['variable2']][2],
                           'series': datarod_ts}

        context = {
            'timeseries_plot': timeseries_plot,
            'plot2': True,
            'datarods_urls_dict': datarods_urls_dict
        }

        return render(request, 'data_rods_explorer/plot.html', context)

    else:
        model = get['model'].upper()
        start_date, end_date, plot_button = plot_ctrls(model, 'plot2')
        select_model2 = SelectInput(display_text='',
                                    name='model2',
                                    multiple=False,
                                    original=True,
                                    options=get_model_options(),
                                    attributes="onchange=oc_model2();"
                                    )
        # Context variables
        context = {
            'start_date': start_date,
            'end_date': end_date,
            'plot_button': plot_button,
            'select_model2': select_model2
        }

    return render(request, 'data_rods_explorer/nav_plot2.html', context)


def years(request):
    """
    Controller for the 'years' page.
    """
    post = request.POST

    # Plot
    if (post and post['prevPlot'] == 'yes') or (post and post['pointLonLat'] != '-9999'):
        varname = get_wms_vars()[post['model']][post['variable']][1]
        varunit = get_wms_vars()[post['model']][post['variable']][2]
        point_lon_lat = post['pointLonLat']
        datarod_ts, datarods_urls_dict = get_data_rod_years(post, point_lon_lat)
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
            'datarods_urls_dict': datarods_urls_dict
        }

        return render(request, 'data_rods_explorer/plot.html', context)

    else:
        # Load page parameters
        years_list = create_years_list(1979)
        select_years = SelectInput(display_text='',
                                   name='years',
                                   multiple=True,
                                   original=False,
                                   options=years_list,
                                   attributes="onchange=oc_years();"
                                   )

        plot_button = Button(display_text='Plot',
                             name='years',
                             style='',
                             icon='',
                             href='',
                             submit=False,
                             disabled=False,
                             attributes='onclick=createPlot(this.name);',
                             classes='')
        # Context variables
        context = {
            'plot_button': plot_button,
            'select_years': select_years
        }

        return render(request, 'data_rods_explorer/nav_years.html', context)


def create_select_model(modelname):
    """
    Function that creates the 'model selection' element
    """
    selected_model = None

    if modelname:
        for model in get_model_options():
            if model[1] == modelname.lower():
                selected_model = model[0]

    select_model = SelectInput(display_text='',
                               name='model',
                               multiple=False,
                               initial=[selected_model if selected_model else None],
                               original=True,
                               options=get_model_options(),
                               attributes="onchange=oc_model();"
                               )
    return select_model


def create_map(layers_ls, req_post):
    """
    Function that creates the 'map' element
    """
    # Center and Zoom level
    if req_post:
        center = [round(float(req_post['centerX']), 4), round(float(req_post['centerY']), 4)]
        if req_post['zoom'] != 'undefined':
            zoom = round(float(req_post['zoom']), 2)
        else:
            zoom = 4
    else:
        center = [-96.5, 38.5]
        zoom = 4
    # Define view options
    view_options = MVView(
        projection='EPSG:4326',
        center=center,
        zoom=zoom,
        maxZoom=10,
        minZoom=1
    )
    # Define map view options
    map_view_options = MapView(
        height='500px',
        width='100%',
        controls=['ZoomSlider'],
        layers=layers_ls,
        view=view_options,
        basemap='OpenStreetMap',
        draw=True,
        legend=True)
    # Return map element
    return [MapView, map_view_options]


def map_date_ctrls(model):
    """
    Function that creates and return the "select_date", "select_hour", and "Display map" elements
    """

    select_date = DatePicker(display_text=False,
                             name='plot_date',
                             autoclose=True,
                             format='mm/dd/yyyy',
                             start_date=get_model_fences()[model]['start_date'],
                             end_date=get_model_fences()[model]['end_date'],
                             start_view=0,
                             attributes='onchange=oc_map_dt();',
                             classes=''
                             )

    select_hour = SelectInput(display_text='',
                              name='plot_hour',
                              multiple=False,
                              original=True,
                              options=[('00:00', '00'), ('01:00', '01'), ('02:00', '02'), ('03:00', '03'),
                                       ('04:00', '04'), ('05:00', '05'), ('06:00', '06'), ('07:00', '07'),
                                       ('08:00', '08'), ('09:00', '09'), ('10:00', '10'), ('11:00', '11'),
                                       ('12:00', '12'), ('13:00', '13'), ('14:00', '14'), ('15:00', '15'),
                                       ('16:00', '16'), ('17:00', '17'), ('18:00', '18'), ('19:00', '19'),
                                       ('20:00', '20'), ('21:00', '21'), ('22:00', '22'), ('23:00', '23')],
                              initial=['00:00'],
                              attributes='onchange=oc_map_dt();',
                              classes=''
                              )

    return [select_date, select_hour]


def plot_ctrls(model, controller):
    """
    Function that creates and return the "start_date", "end_hour", and "plot_button" elements
    """

    differentiator = 1 if controller == 'plot' else 2

    start_date = DatePicker(display_text=False,
                            name='startDate%s' % differentiator,
                            autoclose=True,
                            format='mm/dd/yyyy',
                            start_date=get_model_fences()[model]['start_date'],
                            end_date=get_model_fences()[model]['end_date'],
                            start_view=0,
                            classes='startDate',
                            attributes='onchange=oc_sten_dt("startDate%s");' % differentiator
                            )

    end_date = DatePicker(display_text=False,
                          name='endDate%s' % differentiator,
                          autoclose=True,
                          format='mm/dd/yyyy',
                          start_date=get_model_fences()[model]['start_date'],
                          end_date=get_model_fences()[model]['end_date'],
                          start_view=0,
                          classes='endDate',
                          attributes='onchange=oc_sten_dt("endDate%s");' % differentiator
                          )

    plot_button = Button(display_text='Plot',
                         name=controller,
                         style='',
                         icon='',
                         href='',
                         submit=False,
                         disabled=False,
                         attributes='onclick=createPlot(this.name);',
                         classes='')

    return [start_date, end_date, plot_button]


def create_years_list(first_year=1979):
    """
    This function creates a list of tuples
    with the years available for selection
    """
    years_list = []
    last_year = datetime.now().year
    for yyyy in range(first_year, last_year):
        years_list.append((str(yyyy), str(yyyy)))
    return sorted(years_list, key=lambda year: year[0], reverse=True)


def create_tfw_file(path, lonW, latS, lonE, latN, h=256, w=512):
    hscx = copysign((lonE - lonW)/w, 1)
    hscy = copysign((latN - latS)/h, 1)
    tfw_file = open(path, 'w')
    tfw_file.write('{0}\n'.format(hscx))
    tfw_file.write('0.0\n')
    tfw_file.write('0.0\n')
    tfw_file.write('{0}\n'.format(-hscy))
    tfw_file.write('{0}\n'.format(lonW - hscx/2, lonW))
    tfw_file.write('{0}\n'.format(latN - hscy/2, latN))
    tfw_file.write('')
    tfw_file.close()


def create_prj_file(path):
    """
    This function creates the missing .prj file for the raster
    """
    prj_file = open(path, 'w')
    prj_file.write(('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
                    'SPHEROID["WGS_1984",6378137,298.257223563]],'
                    'PRIMEM["Greenwich",0],'
                    'UNIT["Degree",0.017453292519943295]]'
                    ))
    prj_file.close()


def create_zip_file(zip_path, tiff_path, tfw_path, prj_path):
    """
    this function zips the tiff and prj files into
    """
    zip_file = zipfile.ZipFile(zip_path, "w")
    zip_file.write(tiff_path, arcname=os.path.basename(tiff_path))
    zip_file.write(tfw_path, arcname=os.path.basename(tfw_path))
    zip_file.write(prj_path, arcname=os.path.basename(prj_path))
    zip_file.close()


def get_raster_zip(latlonbox, time_st, model, variable):
    # Parameter
    lonW, latS, lonE, latN = latlonbox

    # Files, paths, and store name & store id
    tiff_file = NamedTemporaryFile(suffix=".tif", delete=False)
    tiff_path = tiff_file.name
    file_name = tiff_file.name[:-4]
    store_name = os.path.basename(file_name)
    store_id = get_workspace() + ':' + store_name
    tfw_path = file_name + '.tfw'
    prj_path = file_name + '.prj'
    zip_path = file_name + '.zip'

    # Create tiff file
    url_image = urllib2.urlopen(get_datarods_png().format(lonW, latS, lonE, latN,
                                                          time_st, get_wms_vars()[model][variable][0]
                                                          ))
    tiff_file.write(url_image.read())
    tiff_file.close()
    # Create prj file
    create_prj_file(prj_path)
    # Create tfw file
    create_tfw_file(tfw_path, float(lonW), float(latS), float(lonE), float(latN))
    create_zip_file(zip_path, tiff_path, tfw_path, prj_path)

    # Return
    return [zip_path, store_name, store_id]


def load_tiff_ly(req_post, req_get):
    """
    This function returns the previously loaded map or the new map layer
    if the button on the page was clicked
    """
    map_layers = []
    add_map = False
    store_id = None

    if req_get and req_get.get('plotTime'):
        plot_time = req_get['plotTime']
    elif req_post and req_post.get('plotTime'):
        plot_time = req_post['plotTime']
    else:
        plot_time = None

    if req_get and req_get.get('model'):
        model = req_get['model']
    elif req_post and req_post.get('model'):
        model = req_post['model']
    else:
        model = None

    if req_get and req_get.get('variable'):
        variable = req_get['variable']
    elif req_post and req_post.get('variable'):
        variable = req_post['variable']
    else:
        variable = None

    if req_post and req_post['loadMap'] != 'no':
        store_id = req_post['loadMap']
        add_map = True
    elif req_get and req_get.get('loadMap') and req_get['loadMap'] != 'no':
        store_id = req_get['loadMap']
        add_map = True

    elif req_post and req_post['retrieveMap'] == 'yes':
        # Geoserver parameters
        geo_eng = get_spatial_dataset_engine(name='default')
        # Data rods parameters
        latlonbox = [req_post['lonW'], req_post['latS'], req_post['lonE'], req_post['latN']]
        time_st = plot_time + ':00:00Z/' + plot_time + ':00:30Z'
        zip_file, store_name, store_id = get_raster_zip(latlonbox, time_st, model, variable)
        # Create raster in geoserver
        response = geo_eng.create_coverage_resource(store_id=store_id,
                                                    coverage_file=zip_file,
                                                    coverage_type='worldimage',
                                                    overwrite=True,
                                                    )
        if response['success']:
            add_map = True

    if add_map:
        # Add raster to map
        title = '{0} {1}'.format(variable, plot_time)
        geoserver_layer = MVLayer(source='ImageWMS',
                                  options={'url': get_geoserver_url(),
                                           'params': {'LAYERS': store_id},
                                           'serverType': 'geoserver'},
                                  legend_title=title,
                                  )
        map_layers = [geoserver_layer]

    return map_layers


def access_datarods_server(link):
    data = []
    error_found = True
    time = 22
    found_data = False
    data_flag_text = 'Date&Time'
    error_flag_text = 'ERROR:'
    error_message = None

    while error_found and time >= 0:
        s_file = urllib2.urlopen(link)
        s_lines = []

        for line in s_file.readlines():
            if data_flag_text in line:
                found_data = True
                error_found = False
                continue

            if not found_data and error_flag_text in line:
                error_message = line
                link = link[:-2] + "%02d" % time
                time -= 1
                break

            if found_data:
                s_lines.append(line)

        s_file.close()

    try:
        if len(s_lines) < 1:
            raise Exception
    except Exception as e:
        e.error = 999
        message = error_message if error_message else 'NASA Data Service Error: Missing "%s” tag to end metadata. ' \
                                                      'See access_datarods_server method in controllers.py for check.' \
                                                      % data_flag_text
        e.message = message
        raise e

    for row in s_lines:
        row_ls = row.strip().replace(' ', '-', 1).split()
        try:
            timevalpair = [parser.parse(row_ls[0]), float(row_ls[1])]
        except Exception as e:
            print str(e)
            continue
        data.append(timevalpair)

    return data


def get_data_rod_plot(req_get, point_lon_lat):
    model = req_get['model']
    variable = req_get['variable']
    superstring = get_datarods_tsb()[model]

    dr_link = superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                 req_get['startDate'], req_get['endDate'])

    dr_ts = access_datarods_server(dr_link)

    datarods_urls_dict = generate_datarods_urls_dict([dr_link])

    return dr_ts, datarods_urls_dict


def get_data_rod_plot2(req_get, point_lon_lat):
    startDate = req_get['startDate']
    endDate = req_get['endDate']

    # 1st variable
    model1 = req_get['model']
    variable1 = req_get['variable']
    superstring1 = get_datarods_tsb()[model1]

    dr_link1 = superstring1.format(variable1, point_lon_lat.replace(',', ',%20'),
                                   startDate, endDate)

    data1 = access_datarods_server(dr_link1)

    # 2nd variable
    model2 = req_get['model2']
    variable2 = req_get['variable2']
    superstring2 = get_datarods_tsb()[model2]

    dr_link2 = superstring2.format(variable2, point_lon_lat.replace(',', ',%20'),
                                   startDate, endDate)
    data2 = access_datarods_server(dr_link2)
    # Create list
    dr_ts = [{'name': get_wms_vars()[model1][variable1][1] + ' (' + get_wms_vars()[model1][variable1][2] + ')',
              'data': data1,
              'code': str(variable1) + ' (' + get_wms_vars()[model1][variable1][2] + ')'},
             {'name': get_wms_vars()[model2][variable2][1] + ' (' + get_wms_vars()[model2][variable2][2] + ')',
              'data': data2,
              'code': str(variable2) + ' (' + get_wms_vars()[model2][variable2][2] + ')'}]

    datarods_urls_dict = generate_datarods_urls_dict([dr_link1, dr_link2])
    return dr_ts, datarods_urls_dict


def get_data_rod_years(req_get, point_lon_lat):
    variable = req_get['variable']
    model = req_get['model']
    superstring = get_datarods_tsb()[model]

    dr_ts = []
    dr_links = []
    for year in req_get['years'].split(','):
        if '-' in year:
            yearRange = year.split('-')
            for yyyy in range(int(yearRange[0]), int(yearRange[1]) + 1):
                dr_link = superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                             '{0}-01-01T00'.format(yyyy),
                                             '{0}-12-31T23'.format(yyyy))
                data = access_datarods_server(dr_link)
                dr_ts.append({'name': yyyy,
                              'data': data})
                dr_links.append(dr_link)
        else:
            dr_link = superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                         '{0}-01-01T00'.format(year),
                                         '{0}-12-31T23'.format(year))

            data = access_datarods_server(dr_link)
            dr_ts.append({'name': year,
                          'data': data})
            dr_links.append(dr_link)

    datarods_urls_dict = generate_datarods_urls_dict(dr_links)

    return dr_ts, datarods_urls_dict


def initialize_model_map_context(get, post):
    # Load model selection, map date and hour, and display map button

    if get and get.get('model'):
        model = get['model']
    elif post and post.get('model'):
        model = post['model']
    else:
        model = get_model_options()[0][1]

    select_model = create_select_model(model)
    select_date, select_hour = map_date_ctrls(model)

    # If 'Display map' is clicked, load layers
    map_layers = load_tiff_ly(post, get)
    if map_layers:
        load_layer = map_layers[0]['options']['params']['LAYERS']
    else:
        load_layer = ''

    # Load map
    MapView, map_view_options = create_map(map_layers, post)

    context = {'select_model': select_model, 'MapView': MapView, 'map_view_options': map_view_options,
               'select_date': select_date, 'select_hour': select_hour, 'map_layers': map_layers,
               'load_layer': load_layer, 'MODEL_FENCES': dumps(get_model_fences())
               }

    return context
