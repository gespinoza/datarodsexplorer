function current_date(day_offset, hh) {
    var today = new Date();
    today.setDate(today.getDate() - day_offset);
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    if (hh === undefined) {
        var hh = today.getHours();
    }
    if (dd<10) {
        dd = '0' + dd;
    }
    if (mm<10) {
        mm = '0' + mm;
    }
    if (hh<10) {
        hh = '0' + hh;
    }
    var date_st = yyyy + '-' + mm  + '-' + dd + 'T' + hh;
    return date_st;
}

function load_variable_options(mod12, var12) {
    var GET = getUrlVars();
    if (GET[mod12]) {
        var model12 = GET[mod12];
        clear_previous_options(var12);
        var vecOption = VAR_DICT[model12];
        var selectElement = document.getElementById(var12);
        for(i=0, l=vecOption.length; i<l; i++) {
            var vec = vecOption[i];
            selectElement.options.add(new Option(vec.text, vec.value, vec.selected));
        }
        if (GET['model'] === GET['model2'] && var12 === 'variable2') {
            remove_variable2_options(GET['variable']);
        }
        selectElement.selectedIndex = 0;
    }
}

function remove_variable2_options(varia) {
    var selectElement = document.getElementById('variable2');
    for (var i=0; i<selectElement.length; i++) {
        if (varia==selectElement.options[i].value) {
            selectElement.remove(i);
        }
    }
}

function clear_previous_options(var12) {
    var selectElement = document.getElementById(var12);
    while(selectElement.options.length>0) {
        selectElement.remove(0);
    }
}

function getUrlVars(href) {
    var vars = {};
    if (href === undefined) {
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
    } else {
        var parts = href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
    }
    return vars;
}

function date_to_rods(st) {
    var dd = st.split('/');
    var ymd = dd[2] + '-' + dd[0] + '-' + dd[1];
    return ymd;
}

function date_to_normal(st) {
    var dd = st.replace('T','-').split('-')
    var mdy = dd[1] + '/' + dd[2] + '/' + dd[0];
    var hh = dd[3];
    var datehour_dict = new Object();
    datehour_dict['date'] = mdy;
    datehour_dict['hour'] = hh;
    return datehour_dict;
}

function getRanges(array) {
    var ranges = [], rstart, rend;
    for (var i = 0; i < array.length; i++) {
        rstart = array[i];
        rend = rstart;
        while (array[i + 1] - array[i] == 1) {
            rend = array[i + 1]; // increment the index if the numbers sequential
            i++;
        }
        ranges.push(rstart == rend ? rstart+'' : rstart + '-' + rend);
    }
    return ranges;
}

function map_click_evt() {
    var map = TETHYS_MAP_VIEW.getMap();
    map.on('singleclick', function(evt) {
        var coords = evt.coordinate;
        //var coords = map.getEventCoordinate(evt);
        var lonlat = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
        //window.alert(lonlat);
        document.getElementById('pointLonLat').value = parseFloat(lonlat[0]).toFixed(4) + ',' + parseFloat(lonlat[1]).toFixed(4);
    });
}

function load_map_post_parameters() {
    var map = TETHYS_MAP_VIEW.getMap();
    var view = map.getView();
    var extent = view.calculateExtent(map.getSize());
    var topleft = ol.proj.toLonLat([extent[0], extent[3]]);
    var bottomright = ol.proj.toLonLat([extent[2], extent[1]]);
    var zoom = view.getZoom();
    var center = ol.proj.toLonLat(view.getCenter());
    document.getElementById('lonW').value = topleft[0];
    document.getElementById('latS').value = bottomright[1];
    document.getElementById('lonE').value = bottomright[0];
    document.getElementById('latN').value = topleft[1];
    document.getElementById('zoom').value = zoom;
    document.getElementById('centerX').value = center[0];
    document.getElementById('centerY').value = center[1];
}

function load_map() {
    document.getElementById('loadMap').value = "no";
    load_map_post_parameters();
    document.getElementById('retrieveMap').value = "yes";
    var data = $('#parametersForm').serialize();
    data += '&plotTime=' + getUrlVars()['plotTime'];
    data += '&variable=' + getUrlVars()['variable'];
    data += '&model=' + getUrlVars()['model'];
    showMapLoading();
    $.ajax({
        url: '/apps/data-rods-explorer/map/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: function (response) {
            hideMapLoading();
            if (response.hasOwnProperty('load_layer')) {
                if (response['load_layer'] !== undefined) {
                    var map = TETHYS_MAP_VIEW.getMap();
                    var lyrParams = {
                        'LAYERS': response['load_layer'],
                        'TILED': true
                    };
                    var newLayer = new ol.layer.Tile({
                        source: new ol.source.TileWMS({
                            url: response['geoserver_url'],
                            params: lyrParams,
                            serverType: 'geoserver'
                        })
                    });
                    map.addLayer(newLayer);
                    newLayer['tethys_legend_title'] = response['load_layer'].split(':')[1];
                    addLegendItem(newLayer);
                    document.getElementById('loadMap').value = response['load_layer'];
                }
            }
        }, error: function () {
            hideMapLoading();
            console.error('Nice try... :(');
        }
    });
    // document.forms['parametersForm'].submit();
}

function createPlot() {
    load_map_post_parameters();
    document.getElementById('retrieveMap').value = "no";
    document.getElementById('prevPlot').value = "yes";

    // document.forms['parametersForm'].submit();
}

function showMapLoading() {
    $('#map-loading')
        .css({
            'height': $('#map_view').height(),
            'width': $('#map_view').width()
        })
        .removeClass('hidden');
}

function hideMapLoading() {
    $('#map-loading').addClass('hidden');
}

function addLegendItem(layer) {
    var title = layer.tethys_legend_title;
    var html =  '<li class="legend-item">' +
        '<div class="legend-buttons">' +
        '<a class="btn btn-default btn-legend-action zoom-control">' + title + '</a>' +
        '<a class="btn btn-default legend-dropdown-toggle">' +
        '<span class="caret"></span>' +
        '<span class="sr-only">Toggle Dropdown</span>' +
        '</a>' +
        '<div class="tethys-legend-dropdown">' +
        '<ul>' +
        '<li><a class="opacity-control">' +
        '<span>Opacity</span> ' +
        '<input type="range" min="0.0" max="1.0" step="0.01" value="' + layer.getOpacity() + '">' +
        '</a></li>' +
        '<li><a class="display-control" href="javascript:void(0);">Hide Layer</a></li>' +
        '</ul>' +
        '</div>' +
        '</div>';

    html += '</li>';

    // Append to the legend items
    $('.legend-items').append(html);

    // Bind events for controls
    last_item = $('.legend-items').children(':last-child');
    menu_toggle_control = $(last_item).find('.legend-dropdown-toggle');
    opacity_control = $(last_item).find('.opacity-control input[type=range]');
    display_control = $(last_item).find('.display-control');
    zoom_control = $(last_item).find('.zoom-control');

    // Bind toggle control
    menu_toggle_control.on('click', function(){
        var dropdown_menu = $(last_item).find('.tethys-legend-dropdown');
        dropdown_menu.toggleClass('open');
    });

    // Bind Opacity Control
    opacity_control.on('input', function() {
        layer.setOpacity(this.value);
    });

    // Bind Display Control
    display_control.on('click', function() {
        if (layer.getVisible()){
            layer.setVisible(false);
            $(this).html('Show Layer');
        } else {
            layer.setVisible(true);
            $(this).html('Hide Layer');
        }
    });

    // Bind Zoom to Layer Control
    zoom_control.on('click', function() {
        var extent;

        extent = layer.tethys_legend_extent;

        if (is_defined(extent)) {
            var lat_lon_extent = ol.proj.transformExtent(extent, layer.tethys_legend_extent_projection, DEFAULT_PROJECTION);
            m_map.getView().fit(lat_lon_extent, m_map.getSize());
        }
    });
}

function is_defined(variable) {
    return !!(typeof variable !== typeof undefined && variable !== false);
}

function updateFences(model) {
    var newEndDate = MODEL_FENCES[model].end_date;
    var newStartDate = MODEL_FENCES[model].start_date;
    $('[data-provide=datepicker]').each(function (idx, elem) {
        if (Date.parse($(elem).val()) > Date.parse(newEndDate)) {
            $(elem).val(newEndDate);
        } else if (Date.parse($(elem).val()) < Date.parse(newStartDate)) {
            $(elem).val(newStartDate);
        }
        $(elem).datepicker('setStartDate', newStartDate);
        $(elem).datepicker('setEndDate', newEndDate);
    });

    var extents = MODEL_FENCES[model].extents;
    var minX = parseFloat(extents.minX);
    var maxX = parseFloat(extents.maxX);
    var minY = parseFloat(extents.minY);
    var maxY = parseFloat(extents.maxY);

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

    MODEL1_LAYER.getSource().clear();
    MODEL1_LAYER.getSource().addFeatures((new ol.format.GeoJSON()).readFeatures(geojsonObject));
}