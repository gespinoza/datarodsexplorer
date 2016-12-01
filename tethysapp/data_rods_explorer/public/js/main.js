$(function() {
    var map;

    $('.app-title').css({'width': '480px'});
    $('#years').select2();
    $('.btn-plot').addClass('disabled');

    map = TETHYS_MAP_VIEW.getMap();
    map.getLayers().item(1).setZIndex(10000);

    map.on('singleclick', function(evt) {
        var coords = evt.coordinate;
        var lonlat = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
        var lon, lat;

        lonlat = convertLonLatToMainMapExtents(lonlat);
        lon = parseFloat(lonlat[0]).toFixed(4);
        lat = parseFloat(lonlat[1]).toFixed(4);
        removeExistingPoint(true);
        addNewPoint(lon, lat, false);
        $('#lon').val(lon);
        $('#lat').val(lat);
    });

    $('#btn-addPoint').on('click', function () {
        var lon = $('#lon').val();
        var lat = $('#lat').val();

        removeExistingPoint();
        addNewPoint(lon, lat, true);
    });

    $('#lon').add('#lat')
        .on('focus', function () {
            $(this).on('keyup', function (e) {
                if (e.which === 13) {
                    $('#btn-addPoint').trigger('click');
                }
            })
        })
        .on('blur', function () {
            $(this).off('keyup');
        });

    // Listener to automatically resize map when the nav bar opens or closes
    (function () {
        var target;
        var observer;
        var config;
        // select the target node to listen for changes
        target = $('#app-content-wrapper')[0];

        observer = new MutationObserver(function () {
            window.setTimeout(function () {
                map.updateSize();
            }, 500);
        });

        config = {attributes: true};

        observer.observe(target, config);
    }());

    $(window).on('resize', function () {
        map.updateSize();
    });

    $('#resetPage').on('click', function () {
        var location = window.location;
        location.href = location.origin + location.pathname;
    });
});