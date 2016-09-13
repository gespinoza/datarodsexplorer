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
    var href = href + '?';
    for (var key in GET) {
        href = href + '&' + key + '=' + GET[key];
    }
    page_and_parameters(href, page);
}

function page_and_parameters(href, page) {
    var GET = getUrlVars();
    // href = href.split('?')[0];
    data = {};

    if (GET['model']) {
        var model = GET['model'];
    } else {
        var model = document.getElementById('model').value;
    }
    data['model'] = model;
    if (GET['variable']) {
        var varia = GET['variable'];
    } else {
        var varia = VAR_DICT[model][0].value;//document.getElementById('variable').value;
    }
    data['variable'] = varia;
    if (GET['plotTime']) {
        var plotDate = GET['plotTime'];
    } else {
        var plotTime = date_to_normal(current_date(140));
        var plotDate = date_to_rods(plotTime['date']) + 'T' + plotTime['hour'];
    }
    data['plotTime'] = plotDate;
    // href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;

    // if (document.getElementById('loadMap').value !== 'no') {
    //     href += '&loadMap=' + document.getElementById('loadMap').value
    // }

    if (page == 'plot') {

        if (GET['endDate']) {
            endDate = GET['endDate'];
        } else {
            var endDate = current_date(133, '23');
        }

        data['endDate'] = endDate;

        if (GET['startDate']) {
            startDate =  GET['startDate'];
        } else {
            var startDate = current_date(140, '0');
        }

        data['startDate'] = startDate;
        // href = href + '&startDate=' + startDate + '&endDate=' + endDate;
    } else if (page == 'plot2') {
        if (GET['model2']) {
            var model2 = GET['model2'];
        } else {
            var model2 = 'nldas'; //1st element
        }

        data['model2'] = model2;

        if (model === model2 && varia == VAR_DICT[model][0].value) {
            var varia2 = VAR_DICT[model2][1].value;
        } else {
            var varia2 = VAR_DICT[model2][0].value;
        }

        data['variable2'] = varia2;

        if (GET['endDate']) {
            endDate = GET['endDate'];
        } else {
            var endDate = current_date(133, '23');
        }

        data['endDate'] = endDate;

        if (GET['startDate']) {
            startDate =  GET['startDate'];
        } else {
            var startDate = current_date(140, '0');
        }

        data['startDate'] = startDate;

        // href = href + '&model2=' + model2 + '&variable2=' + varia2 + '&startDate=' + startDate + '&endDate=' + endDate;
    } else if (page == 'years') {
        var endDate = current_date(140, '23');
        years = endDate.substr(0, 4);
        // href =  href + '&years=' + years;
        data['years'] = years;
    }
    // window.location = href;
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
                load_variable_options('model2', 'variable2');
            } else if (page == 'years') {
                $('#nav-years').html(htmlResponse);
                load_default_years(data);
            }
            addVarsToURL(data);
        },
        error: function () {
            console.error('Nice try... :(');
        }
    })
}

function load_default_home(modelFencesEncoded) {
    var modelFencesStr = modelFencesEncoded.replace(/&quot;/g, '"');
    MODEL_FENCES = JSON.parse(modelFencesStr);
    var counter = 0;
    var GET = getUrlVars();
    var href = window.location.href.split('?')[0];

    if (GET['model']) {
        var model = GET['model'];
    } else {
        var model = document.getElementById('model').value;
        counter = counter + 1;
    }
    if (GET['variable']) {
        var varia = GET['variable'];
    } else {
        var varia = VAR_DICT[model][0].value;//document.getElementById('variable').value;
        counter = counter + 1;
    }
    if (GET['plotTime']) {
        var plotTime = date_to_normal(GET['plotTime']);
    } else {
        var plotTime = {};
        plotTime['date'] = MODEL_FENCES[model.toUpperCase()].end_date;
        plotTime['hour'] = '00';
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        $('#plot_date').data('start_date', MODEL_FENCES[model.toUpperCase()].start_date);
        counter = counter + 1;
    }

    if (counter > 0) {
        var plotDate = date_to_rods(plotTime['date']);
        plotDate = plotDate + 'T' + plotTime['hour'];
        href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
        window.location = href;
    } else {
        document.getElementById('model').value = model;
        document.getElementById('variable').value = varia;
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
    }

    load_extents_layer(model.toUpperCase())
}

function load_default_plot(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href; //.split('?')[0]
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
    if (GET['startDate']) {
        var startDate = date_to_normal(GET['startDate']);
    } else {
        counter = counter + 1;
    }
    if (GET['endDate']) {
        var endDate = date_to_normal(GET['endDate']);
    } else {
        counter = counter + 1;
    }

    if (counter > 0) {
        page_and_parameters(href, 'plot');
    } else {
        // document.getElementById('model').value = model;
        // document.getElementById('variable').value = varia;
        // document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        document.getElementById('startDate').value = startDate['date'];
        document.getElementById('endDate').value = endDate['date'];
    }
}

function load_default_plot2(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href; //.split('?')[0]
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
    if (GET['model2']) {
        var model2 = GET['model2'];
    } else {
        counter = counter + 1;
    }
    if (GET['variable2']) {
        var varia2 = GET['variable2'];
    } else {
        counter = counter + 1;
    }
    if (GET['plotTime']) {
        var plotTime = date_to_normal(GET['plotTime']);
    } else {
        counter = counter + 1;
    }
    if (GET['startDate']) {
        var startDate = date_to_normal(GET['startDate']);
    } else {
        counter = counter + 1;
    }
    if (GET['endDate']) {
        var endDate = date_to_normal(GET['endDate']);
    } else {
        counter = counter + 1;
    }

    if (counter > 0) {
        page_and_parameters(href, 'plot2');
    } else {
        document.getElementById('model').value = model;
        document.getElementById('variable').value = varia;
        document.getElementById('model2').value = model2;
        document.getElementById('variable2').value = varia2;
        document.getElementById('plot_date').value = plotTime['date'];
        document.getElementById('plot_hour').value = plotTime['hour'];
        document.getElementById('startDate').value = startDate['date'];
        document.getElementById('endDate').value = endDate['date'];
    }
}

function load_default_years(data) {
    var counter = 0;
    var GET = data ? data : getUrlVars();
    var href = window.location.href; //.split('?')[0]
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
        for (var i=0; i < years_list.length; i++) {
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
        for (var i=0; i < years_options.length; i++) {
            if (years_array.indexOf(years_options[i].value) != -1) {
                years_options[i].selected = true;
            }
        }
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

function load_extents_layer(model) {
    $(function () {
        var extents = MODEL_FENCES[model].extents;
        var minX = parseFloat(extents.minX);
        var maxX = parseFloat(extents.maxX);
        var minY = parseFloat(extents.minY);
        var maxY = parseFloat(extents.maxY);
        var map = TETHYS_MAP_VIEW.getMap();

        var style = new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'blue',
                width: 3
            }),
            fill: new ol.style.Fill({
                color: 'rgba(0, 0, 255, 0.1)'
            })
        });

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

        var source = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(geojsonObject)
        });

        MODEL1_LAYER = new ol.layer.Vector({
            source: source,
            style: style
        });
        map.addLayer(MODEL1_LAYER);
        MODEL1_LAYER['tethys_legend_title'] = 'Model 1 Extents';
        addLegendItem(MODEL1_LAYER);
    });
}