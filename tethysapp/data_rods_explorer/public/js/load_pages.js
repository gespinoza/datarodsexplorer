function onClickLink(link, href, page) {
    if ($(link).hasClass('open')) {
        $('#nav-' + page).html('');
        $(link).removeClass('open');
    } else {
        page_and_parameters(href, page);
        $(link).addClass('open');
    }
}

function page_and_parameters_html(href, page) {
    var GET = getUrlVars();
    href = href + '?';

    Object.keys(GET).forEach(function (key) {
        href = href + '&' + key + '=' + GET[key];
    });

    page_and_parameters(href, page);
}

function page_and_parameters(href, page) {
    var GET = getUrlVars();
    var data = {};
    var model, varia, plotDate, plotTime, endDate, startDate, model2, varia2, years;

    if (GET['model']) {
        model = GET['model'];
    } else {
        model = document.getElementById('model').value;
    }

    if (GET['variable']) {
        varia = GET['variable'];
    } else {
        varia = VAR_DICT[model][0].value;
    }

    if (GET['plotTime']) {
        plotDate = GET['plotTime'];
    } else {
        plotTime = date_to_normal(current_date(140));
        plotDate = date_to_rods(plotTime['date']) + 'T' + plotTime['hour'];
    }

    data = {
        'model': model,
        'variable': varia,
        'plotTime': plotDate
    };

    if (page.indexOf('plot') !== -1) {

        if (GET['endDate']) {
            endDate = GET['endDate'];
        } else {
            endDate = getValidDate(plotDate, model);
        }

        data['endDate'] = endDate;

        if (GET['startDate']) {
            startDate =  GET['startDate'];
        } else {
            startDate = get_date_of_days_before(endDate, 7).toISOString().split('T')[0] + 'T00';
        }

        data['startDate'] = startDate;

        if (page == 'plot2') {
            if (GET['model2']) {
                model2 = GET['model2'];
            } else {
                model2 = 'NLDASF'; //1st element
            }

            data['model2'] = model2;

            if (model === model2 && varia == VAR_DICT[model][0].value) {
                varia2 = VAR_DICT[model2][1].value;
            } else {
                varia2 = VAR_DICT[model2][0].value;
            }

            data['variable2'] = varia2;
        }

    } else if (page == 'years') {
        endDate = current_date(140, '23');
        years = endDate.substr(0, 4);

        data['years'] = years;
    }

    $.ajax({
        url: href,
        type: 'GET',
        data: data,
        dataType: 'html',
        success: function (htmlResponse) {
            if (page == 'plot') {
                $('#nav-plot').html(htmlResponse);
                load_default_plot(data);
            } else if (page == 'plot2') {
                $('#nav-plot2').html(htmlResponse);
                load_default_plot2(data);
                load_variable_options('model2', 'variable2', data);
            } else if (page == 'years') {
                $('#nav-years').html(htmlResponse);
                $('#years').select2();
                load_default_years(data);
            }
            disablePlotButtonIfNeeded();
            addVarsToURL(data);
        },
        error: function () {
            console.error('Nice try... :(');
        }
    })
}

function load_default_home() {
    var counter = 0;
    var GET = getUrlVars();
    var href = window.location.href.split('?')[0];
    var model, varia, plotTime, plotDate;

    if (GET['model']) {
        model = GET['model'];
    } else {
        model = document.getElementById('model').value;
        counter = counter + 1;
    }

    if (GET['variable']) {
        varia = GET['variable'];
    } else {
        varia = VAR_DICT[model][0].value;
        counter = counter + 1;
    }

    if (GET['plotTime']) {
        plotTime = date_to_normal(GET['plotTime']);
    } else {
        plotTime = {};
        plotTime['date'] = MODEL_FENCES[model]['end_date'];
        plotTime['hour'] = '00';
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        $('#plot_date').data('start_date', MODEL_FENCES[model]['start_date']);
        counter = counter + 1;
    }

    if (counter > 0) {
        plotDate = date_to_rods(plotTime['date']);
        plotDate = plotDate + 'T' + plotTime['hour'];
        href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
        window.history.pushState({}, 'None', href);
        load_default_home()
    } else {
        document.getElementById('model').value = model;
        document.getElementById('variable').value = varia;
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        load_extents_layers(model)
    }
}

function load_default_plot(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href;
    var startDate, endDate;

    if (GET['startDate']) {
        startDate = date_to_normal(GET['startDate']);
    } else {
        counter = counter + 1;
    }

    if (GET['endDate']) {
        endDate = date_to_normal(GET['endDate']);
    } else {
        counter = counter + 1;
    }

    if (counter > 0) {
        page_and_parameters(href, 'plot');
    } else {
        document.getElementById('startDate1').value = startDate['date'];
        document.getElementById('endDate1').value = endDate['date'];
    }
}

function load_default_plot2(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href; //.split('?')[0]
    var model2, varia2, startDate, endDate;

    if (GET['model2']) {
        model2 = GET['model2'];
    } else {
        counter = counter + 1;
    }

    if (GET['variable2']) {
        varia2 = GET['variable2'];
    } else {
        counter = counter + 1;
    }

    if (GET['startDate']) {
        startDate = date_to_normal(GET['startDate']);
    } else {
        counter = counter + 1;
    }

    if (GET['endDate']) {
        endDate = date_to_normal(GET['endDate']);
    } else {
        counter = counter + 1;
    }

    if (counter > 0) {
        page_and_parameters(href, 'plot2');
    } else {
        document.getElementById('model2').value = model2;
        document.getElementById('variable2').value = varia2;
        document.getElementById('startDate2').value = startDate['date'];
        document.getElementById('endDate2').value = endDate['date'];
    }
}

function load_default_years(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href;
    if (GET['model']) {
        var model = GET['model'];
    } else {
        counter = counter + 1;
    }
    if (GET['variable']) {
        var varia = GET['variable'];
    } else {
        counter = counter + 1;
    }
    if (GET['plotTime']) {
        var plotTime = date_to_normal(GET['plotTime']);
    } else {
        counter = counter + 1;
    }
    if (GET['years']) {
        var years = GET['years'];
    } else {
        counter = counter + 1;
    }

    if (counter > 0) {
        page_and_parameters(href, 'years');
    } else {
        document.getElementById('model').value = model;
        document.getElementById('variable').value = varia;
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        //from here the code is new
        var years_list = years.split(',');
        var years_array = [];
        var i;

        for (i = 0; i < years_list.length; i++) {
            if (years_list[i].indexOf('-') === -1) {
                years_array = years_array.concat(years_list[i])
            } else {
                var start_yy = parseInt(years_list[i].split('-')[0]);
                var end_yy = parseInt(years_list[i].split('-')[1]);
                for (start_yy; start_yy <= end_yy; start_yy++) {
                    years_array = years_array.concat(start_yy.toString());
                }
            }
        }

        var years_options = document.getElementById('years');

        for (i = 0; i < years_options.length; i++) {
            if (years_array.indexOf(years_options[i].value) != -1) {
                years_options[i].selected = true;
            }
        }

        $('#years').trigger('change');
    }
}

function addVarsToURL(vars) {
    var href = window.location.href.split('?')[0] + '?';
    Object.keys(vars).forEach(function (key) {
        href = href + key + '=' + vars[key] + '&';
    });
    href = href.slice(0, -1);
    window.history.pushState({}, 'None', href);
}

function load_extents_layers(model) {
    $(function () {
        var extents = validateExtents(MODEL_FENCES[model].extents);
        var minX = parseFloat(extents.minX);
        var maxX = parseFloat(extents.maxX);
        var minY = parseFloat(extents.minY);
        var maxY = parseFloat(extents.maxY);
        var map = TETHYS_MAP_VIEW.getMap();

        var getStyle = function (layer) {
            var strokeColor = layer === 1 ? 'blue' : 'red';
            var fillColor = layer === 1 ? 'rgba(0, 0, 255, 0.1)' : 'rgba(255, 0, 0, 0.1)';

            return new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: strokeColor,
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: fillColor
                })
            });
        };

        var geojsonObject = {
            'type': 'FeatureCollection',
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:4326'
                }
            },
            'features': [{
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        ol.proj.fromLonLat([minX, maxY]),
                        ol.proj.fromLonLat([maxX, maxY]),
                        ol.proj.fromLonLat([maxX, minY]),
                        ol.proj.fromLonLat([minX, minY]),
                        ol.proj.fromLonLat([minX, maxY])
                    ]]
                }
            }]
        };

        var source1 = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(geojsonObject)
        });

        var source2 = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(geojsonObject)
        });

        var olExtents = [minX, minY, maxX, maxY];
        var olProjection = 'EPSG:4326';

        MODEL1_LAYER = new ol.layer.Vector({
            source: source1,
            style: getStyle(1),
            name: 'model1_extents',
            extent: olExtents
        });
        MODEL2_LAYER = new ol.layer.Vector({
            source: source2,
            style: getStyle(2),
            name: 'model2_extents',
            extent: olExtents
        });
        map.addLayer(MODEL1_LAYER);
        map.addLayer(MODEL2_LAYER);
        MODEL1_LAYER['tethys_legend_title'] = 'Model 1 Extents';
        MODEL2_LAYER['tethys_legend_title'] = 'Model 2 Extents';
        MODEL1_LAYER['tethys_legend_extent'] = olExtents;
        MODEL2_LAYER['tethys_legend_extent'] = olExtents;
        MODEL1_LAYER['tethys_legend_extent_projection'] = olProjection;
        MODEL2_LAYER['tethys_legend_extent_projection'] = olProjection;

        update_legend();
    });
}