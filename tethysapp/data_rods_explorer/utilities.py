# coding=utf-8
import urllib.request, urllib.error, urllib.parse
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
                               attributes="onchange=oc_model();"
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
        height='500px',
        width='100%',
        controls=['ZoomSlider'],
        layers=[],
        view=view_options,
        basemap='OpenStreetMap',
        draw=draw_options,
        legend=True,
        disable_basemap=False,

    )
    # Return map element
    return [MapView, map_view_options]


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


def get_data_from_nasa_server(link, overlap_years=False):
    data = []
    error_found = True
    time = 22
    found_data = False
    data_flag_text = 'Date&Time'
    error_flag_text = 'ERROR:'
    nasa_error_message = None
    custom_error_message = ('ERROR 999: Data returned by NASA was either missing the expected "%s” line to '
                            'indicate the start of the data, or returned with an empty dataset.'
                            % data_flag_text)
    s_lines = []

    while error_found and time >= 0:
        nasa_error_message = None
        s_file = urllib.request.urlopen(link)

        for line in s_file.readlines():
            if data_flag_text.encode() in line:
                found_data = True
                error_found = False
                continue

            if not found_data and error_flag_text.encode() in line:
                nasa_error_message = line
                link = link[:-2] + "%02d" % time
                time -= 1
                break

            if found_data:
                s_lines.append(line)

        s_file.close()

    if len(s_lines) < 1:
        raise Exception(custom_error_message)
    elif nasa_error_message:
        raise Exception(nasa_error_message)

    for row in s_lines:
        row_ls = row.strip()
        row_ls = row_ls.decode().replace(' ', '-', 1)
        row_ls = row_ls.split()
        try:
            date = '2000' + row_ls[0][4:] if overlap_years else row_ls[0]
            val = row_ls[1]
            date_val_pair = [dateparser.parse(date), float(val)]
        except Exception as e:
            print(str(e))
            continue
        data.append(date_val_pair)

    return data


def get_data_rod_plot(req_get, point_lon_lat):
    model = req_get['model']
    variable = req_get['variable']
    superstring = get_datarods_tsb()[model]

    dr_link = str(superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                     req_get['startDate'], req_get['endDate']))

    dr_ts = get_data_from_nasa_server(dr_link)

    datarods_urls_dict = generate_datarods_urls_dict([dr_link])

    return dr_ts, datarods_urls_dict


def get_data_rod_plot2(req_get, point_lon_lat):
    start_date = req_get['startDate']
    end_date = req_get['endDate']

    # 1st variable
    model1 = req_get['model']
    variable1 = req_get['variable']
    superstring1 = get_datarods_tsb()[model1]

    dr_link1 = str(superstring1.format(variable1, point_lon_lat.replace(',', ',%20'),
                                       start_date, end_date))

    data1 = get_data_from_nasa_server(dr_link1)

    # 2nd variable
    model2 = req_get['model2']
    variable2 = req_get['variable2']
    superstring2 = get_datarods_tsb()[model2]

    dr_link2 = str(superstring2.format(variable2, point_lon_lat.replace(',', ',%20'),
                                       start_date, end_date))
    data2 = get_data_from_nasa_server(dr_link2)
    # Create list
    dr_ts = [{'name': get_wms_vars()[model1][variable1][1] + ' (' + get_wms_vars()[model1][variable1][2] + ')',
              'data': data1,
              'code': str(variable1) + ' (' + get_wms_vars()[model1][variable1][2] + ')'},
             {'name': get_wms_vars()[model2][variable2][1] + ' (' + get_wms_vars()[model2][variable2][2] + ')',
              'data': data2,
              'code': str(variable2) + ' (' + get_wms_vars()[model2][variable2][2] + ')'}]

    datarods_urls_dict = generate_datarods_urls_dict([dr_link1, dr_link2])
    return dr_ts, datarods_urls_dict


def get_data_rod_years(req_post, point_lon_lat):
    variable = req_post['variable']
    model = req_post['model']
    superstring = get_datarods_tsb()[model]
    overlap_years = True if 'true' in req_post['overlap_years'] else False

    dr_ts = []
    dr_links = []
    for year in req_post['years'].split(','):
        if '-' in year:
            year_range = year.split('-')
            for yyyy in range(int(year_range[0]), int(year_range[1]) + 1):
                dr_link = superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                             '{0}-01-01T00'.format(yyyy),
                                             '{0}-12-31T23'.format(yyyy))
                data = get_data_from_nasa_server(dr_link, overlap_years)
                dr_ts.append({'name': yyyy,
                              'data': data})
                dr_links.append(dr_link)
        else:
            dr_link = str(superstring.format(variable, point_lon_lat.replace(',', ',%20'),
                                             '{0}-01-01T00'.format(year),
                                             '{0}-12-31T23'.format(year)))

            data = get_data_from_nasa_server(dr_link, overlap_years)
            dr_ts.append({'name': year,
                          'data': data})
            dr_links.append(dr_link)

    datarods_urls_dict = generate_datarods_urls_dict(dr_links)

    return dr_ts, datarods_urls_dict


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
