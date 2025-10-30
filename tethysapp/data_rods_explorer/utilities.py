# coding=utf-8
import netrc
import io
import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from dateutil import parser as dateparser
from .model_objects import get_wms_vars, get_datarods_tsb, \
    get_model_fences, get_model_options
from tethys_sdk.gizmos import SelectInput, MapView, MVView, DatePicker, Button, MVDraw


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
                               name='model1',
                               multiple=False,
                               initial=[selected_model if selected_model else None],
                               original=True,
                               options=get_model_options(),
                               attributes="onchange=oc_model();",
                               classes="w-100 mb-3 form-control"
                               )
    return select_model


def create_map():
    """
    Function that creates the 'map' element
    """
    # Center and Zoom level
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
    draw_options = MVDraw(
        controls=["Pan"],
        feature_selection=False,
        point_color='yellow',

    )
    # Define map view options
    map_view_options = MapView(
        height='100%',
        width='100%',
        controls=['ZoomSlider'],
        layers=[],
        view=view_options,
        basemap=['OpenStreetMap',],
        draw=draw_options,
        legend=True,
        disable_basemap=False,

    )
    # Return map element
    return map_view_options


def create_map_date_ctrls(model):
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
                             classes='mb-3'
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
                              classes='form-control'
                              )

    return [select_date, select_hour]


def create_plot_ctrls(model, controller):
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
                         classes='btn-plot')

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

def normalize_time_string(time_string):
    return datetime.strptime(time_string, "%Y-%m-%dT%H").strftime("%Y-%m-%dT%H:%M:%S")

def get_data_from_nasa_server(request_params, overlap_years=False, full_output=False):
    time_series_url = "https://api.giovanni.earthdata.nasa.gov/timeseries"

    lon = request_params['lon']
    lat = request_params['lat']
    time_start = normalize_time_string(request_params['start_date'])
    time_end = normalize_time_string(request_params['end_date'])
    data = request_params['plot_variable']
    
    headers = {"authorizationtoken": get_earthdata_token()}

    query_parameters = {
            "data": data,
            "location": f"[{float(lat)}, {float(lon)}]",
            "time": f"{time_start}/{time_end}",
        }

    if full_output:
        response = requests.get(time_series_url, params=query_parameters, headers=headers, stream=True)

        if response.status_code != 200:
            raise Exception(
                f"ERROR {response.status_code}: NASA GiC service returned an error for {lat},{lon} parameter '{data}'."
            )
        return {"content": response.content, "content_type": response.headers.get('Content-Type', 'application/octet-stream')}

    else:
        response = requests.get(time_series_url, params=query_parameters, headers=headers)

        data_list = []

        with io.StringIO(response.text) as f:
            for line in f:
                if line.strip().startswith("Timestamp"):
                    break

            for line in f:
                if not line.strip():
                    continue

                parts = line.strip().split(",")
                if len(parts) < 2:
                    continue

                date = parts[0]
                value = float(parts[1])

                try:
                    if overlap_years:
                        date = "2000" + date[4:]
                    date = dateparser.parse(date)
                    data_list.append([date, value])
                except Exception:
                    continue
                
        if not data_list:
            raise Exception(
                f"ERROR 999: NASA GiC service returned no usable data for {lat},{lon} parameter '{data}'."
            )
        
        return data_list


def get_data_rod_plot(req_get, point_lon_lat):
    lon, lat = point_lon_lat.split(',')

    request_params = {
        "plot_variable": req_get['plot_variable'],
        "lon": lon,
        "lat": lat,
        "start_date": req_get['startDate'],
        "end_date": req_get['endDate'],
    }
    dr_ts = get_data_from_nasa_server(request_params)

    return dr_ts


def get_data_rod_plot2(req_get, point_lon_lat):
    lon, lat = point_lon_lat.split(',')

    request_params_1 = {
        "plot_variable": req_get['plot_variable'],
        "lon": lon,
        "lat": lat,
        "start_date": req_get['startDate'],
        "end_date": req_get['endDate']
    }

    data1 = get_data_from_nasa_server(request_params_1)

    request_params_2 = {
        "plot_variable" : req_get['plot_variable2'],
        "lon": lon,
        "lat": lat,
        "start_date": req_get['startDate'],
        "end_date": req_get['endDate'],
    }

    data2 = get_data_from_nasa_server(request_params_2)


    model1 = req_get['model']
    model2 = req_get['model2']

    variable1 = req_get['map_variable']
    variable2 = req_get['map_variable2']

    # Create list
    dr_ts = [{'name': get_wms_vars()[model1][variable1][1] + ' (' + get_wms_vars()[model1][variable1][2] + ')',
              'data': data1,
              'code': str(variable1) + ' (' + get_wms_vars()[model1][variable1][2] + ')'},
             {'name': get_wms_vars()[model2][variable2][1] + ' (' + get_wms_vars()[model2][variable2][2] + ')',
              'data': data2,
              'code': str(variable2) + ' (' + get_wms_vars()[model2][variable2][2] + ')'}]

    return dr_ts

def get_data_rod_years(req_post, point_lon_lat):
    variable = req_post['plot_variable']
    lon, lat = point_lon_lat.split(',')
    if 'overlap_years' in req_post:
        overlap_years = True if 'true' in req_post['overlap_years'] else False
    else:
        overlap_years = False
        
    dr_ts = []
    for year in req_post['years'].split(','):
        if '-' in year:
            year_range = year.split('-')
            for yyyy in range(int(year_range[0]), int(year_range[1]) + 1):
                start_date = '{0}-01-01T00'.format(yyyy)
                end_date = '{0}-12-31T23'.format(yyyy)
                request_params = {
                    "plot_variable": variable,
                    "lon": lon,
                    "lat": lat,
                    "start_date": start_date,
                    "end_date": end_date,
                }

                data = get_data_from_nasa_server(request_params, overlap_years=overlap_years)
                dr_ts.append({'name': yyyy,
                              'data': data})
        else:
            start_date = '{0}-01-01T00'.format(year)
            end_date = '{0}-12-31T23'.format(year)
            request_params = {
                "plot_variable": variable,
                "lon": lon,
                "lat": lat,
                "start_date": start_date,
                "end_date": end_date,
            }

            data = get_data_from_nasa_server(request_params, overlap_years=overlap_years)
            dr_ts.append({'name': year,
                          'data': data})

    return dr_ts


def generate_datarods_urls_dict(asc2_urls):
    plot_urls = []
    waterml_urls = []
    netcdf_urls = []

    for url in asc2_urls:
        plot_urls.append(url.replace('asc2', 'plot'))
        waterml_urls.append(url.replace('asc2', 'waterml'))
        netcdf_urls.append(url.replace('asc2', 'netcdf'))

    return {
        'asc2': asc2_urls,
        'plot': plot_urls,
        'waterml': waterml_urls,
        'netcdf': netcdf_urls
    }

def get_earthdata_token():
    url = "https://api.giovanni.earthdata.nasa.gov/signin"
    token = requests.get(url, auth=HTTPBasicAuth(netrc.netrc().hosts["urs.earthdata.nasa.gov"][0],
                         netrc.netrc().hosts["urs.earthdata.nasa.gov"][2]),
                         allow_redirects=True).text.replace('"','')
    return token

def format_csv_data(raw_data):
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode('utf-8')
        
    lines = raw_data.strip().splitlines()
    meta_lines = []
    data_lines = []

    # Separate metadata from data
    for i, line in enumerate(lines):
        if line.startswith("Timestamp"):
            meta_lines = lines[:i]
            data_lines = lines[i:]
            break

    # Pretty print metadata
    formatted_meta = "\n".join(f"{k.strip():<20} {v.strip()}" for k, v in 
                               (m.split(",", 1) for m in meta_lines if "," in m))

    # Add spacing and simple column headers
    formatted_data = "\n".join(data_lines)

    return f"{formatted_meta}\n\n{formatted_data}"