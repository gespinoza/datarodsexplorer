function onClickLink(link, navItem) {
    if ($(link).hasClass('open')) {
        $(link).removeClass('open');
        $('#nav-' + navItem).addClass('hidden');

        if (navItem == 'plot2') {
            removeFlashMessage('bound-adjusted');
            TETHYS_MAP_VIEW.getMap().removeLayer(MODEL2_LAYER);
            update_legend();
            COMPARE_TWO = false;
        }
    } else {
        $('.nav-link').removeClass('open');
        $(link).addClass('open');
        $('.nav-item').addClass('hidden');
        $('#nav-' + navItem).removeClass('hidden');

        loadNavOptionsAndParams(navItem);

        if (navItem == 'plot2') {
            TETHYS_MAP_VIEW.getMap().addLayer(MODEL2_LAYER);
            update_legend();
            COMPARE_TWO = true;
        } else {
            removeFlashMessage('bound-adjusted');
            TETHYS_MAP_VIEW.getMap().removeLayer(MODEL2_LAYER);
            update_legend();
            COMPARE_TWO = false;
        }
        validateClickPoint()
    }
}

function loadNavOptionsAndParams(navItem) {
    var GET = getUrlVars();
    var data, model, varia, plotDate, plotTime, endDate, startDate, model2, varia2, years;

    if (GET['model']) {
        model = GET['model'];
    } else {
        model = $('#model1').val();
    }

    if (GET['variable']) {
        varia = GET['variable'];
    } else {
        varia = VAR_DICT[model][0].value;
    }

    if (GET['plotTime']) {
        plotDate = GET['plotTime'];
    } else {
        plotTime = rodsDateToDateHourPickerDict(current_date(140));
        plotDate = dateHourPickerToRodsDate(plotTime['date']) + 'T' + plotTime['hour'];
    }

    data = {
        'model': model,
        'variable': varia,
        'plotTime': plotDate
    };

    // Keep lon, lat in URL if already there
    if (GET['lon']) {
        data['lon'] = GET['lon'];
    }

    if (GET['lat']) {
        data['lat'] = GET['lat'];
    }

    if (navItem.indexOf('plot') !== -1) {

        if (GET['endDate']) {
            endDate = GET['endDate'];
        } else {
            endDate = getValidRodsDate(plotDate, model);
        }

        data['endDate'] = endDate;

        if (GET['startDate']) {
            startDate =  GET['startDate'];
        } else {
            startDate = getPrevRodsDate(endDate, 7);
        }

        data['startDate'] = startDate;

        if (navItem == 'plot2') {
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

    } else if (navItem == 'years') {
        if (GET['years']) {
            years = GET['years'];
            data['years'] = years;
        }
    }
    if (navItem == 'plot') {
        loadDefaultsForPlotNav(data);
    } else if (navItem == 'plot2') {
        loadDefaultsForPlot2Nav(data);
        loadVariableOptions('model2', 'variable2', data);
    } else if (navItem == 'years') {
        loadDefaultsForYearsNav(data);
    }
    addVarsToURL(data);
}

function loadDefaultHome() {
    var href;
    var GET = getUrlVars();
    var model = GET['model'];
    var plotTime = {};
    var lon = GET['lon'];
    var lat = GET['lat'];
    var navItem;

    if (model === undefined) {
        model = $('#model1').val();
        GET['model'] = model;
    }

    if (GET['variable'] === undefined) {
        GET['variable'] = VAR_DICT[model][0].value;
    }

    if (GET['plotTime']) {
        plotTime = rodsDateToDateHourPickerDict(GET['plotTime']);
    } else {
        plotTime['date'] = MODEL_FENCES[model]['end_date'];
        plotTime['hour'] = '00';
        GET['plotTime'] = dateHourPickerToRodsDate(plotTime['date'], plotTime['hour'])
    }

    $('#model1').val(model);
    $('#variable').val(GET['variable']);
    $('#plot_date').val(plotTime['date']);
    $('#plot_hour').val(plotTime['hour']);

    if (lon !== undefined) {
        $('#lon').val(lon)
    }

    if (lat !== undefined) {
        $('#lat').val(lat)
    }

    if (lon !== undefined && lat !== undefined) {
        addNewPoint(Number(lon), Number(lat), true);
    }

    href = constructHref(GET);
    window.history.pushState({}, 'None', href);

    if (GET['years'] !== undefined) {
        navItem = 'years';
    } else if (GET['variable2'] !== undefined) {
        navItem = 'plot2'
    } else if (GET['startDate'] !== undefined) {
        navItem = 'plot'
    }

    // Must be called before the onClickLink() function
    loadExtentsLayers(model);

    if (navItem) {
        onClickLink($('#nav-' + navItem).prev().children()[0], navItem);
    }
}

function loadDefaultsForPlotNav(data) {
    var GET = data ? data : getUrlVars();
    var startDate, endDate;

    if (GET['endDate']) {
        endDate = GET['endDate'];
    } else {
        endDate = getValidRodsDate(GET['plotDate'], model);
    }

    if (GET['startDate']) {
        startDate =  GET['startDate'];
    } else {
        startDate = getPrevRodsDate(endDate, 7);
    }

    $('#startDate1').val(rodsDateToDateHourPickerDict(startDate)['date']);
    $('#endDate1').val(rodsDateToDateHourPickerDict(endDate)['date']);

    updateTemporalFences();
}

function loadDefaultsForPlot2Nav(data) {
    var GET = data ? data : getUrlVars();
    var model2, varia2, startDate, endDate;

    if (GET['model2']) {
        model2 = GET['model2'];
    } else {
        model2 = 'NLDASF'; //1st element
    }

    if (GET['endDate']) {
        endDate = GET['endDate'];
    } else {
        endDate = getValidRodsDate(get['plotDate'], model2);
    }

    if (GET['startDate']) {
        startDate =  GET['startDate'];
    } else {
        startDate = getPrevRodsDate(endDate, 7);
    }

    if (GET['model'] === model2 && GET['variable'] == VAR_DICT[GET['model']][0].value) {
        varia2 = VAR_DICT[model2][1].value;
    } else {
        varia2 = VAR_DICT[model2][0].value;
    }

    $('#model2').val(model2);
    $('#variable2').val(varia2);
    $('#startDate2').val(rodsDateToDateHourPickerDict(startDate)['date']);
    $('#endDate2').val(rodsDateToDateHourPickerDict(endDate)['date']);

    updateTemporalFences();
}

function loadDefaultsForYearsNav(data) {
    var GET = data ? data : getUrlVars();
    var years;

    if (GET['years']) {
        $('#years')
            .val(GET['years'].split(','))
            .trigger('change');
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

function loadExtentsLayers(model) {

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
    });
    MODEL2_LAYER = new ol.layer.Vector({
        source: source2,
        style: getStyle(2),
        name: 'model2_extents',
    });
    MODEL1_LAYER['tethys_legend_title'] = 'Model 1 Extents';
    MODEL2_LAYER['tethys_legend_title'] = 'Model 2 Extents';
    MODEL1_LAYER['tethys_legend_extent'] = olExtents;
    MODEL2_LAYER['tethys_legend_extent'] = olExtents;
    MODEL1_LAYER['tethys_legend_extent_projection'] = olProjection;
    MODEL2_LAYER['tethys_legend_extent_projection'] = olProjection;
    map.addLayer(MODEL1_LAYER);
    update_legend();
}