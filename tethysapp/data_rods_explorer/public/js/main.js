$(function() {
    var map = TETHYS_MAP_VIEW.getMap();
    map.on('singleclick', function(evt) {
        removeFlashMessage('click-map');
        var pointSource = map.getLayers().item(1).getSource();

        while (pointSource.getFeatures().length > 1) {
            pointSource.removeFeature(pointSource.getFeatures()[0]);
        }

        var coords = evt.coordinate;
        var lonlat = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
        lonlat = convertLonLatToMainMapExtents(lonlat);
        document.getElementById('pointLonLat').value = parseFloat(lonlat[0]).toFixed(4) + ',' + parseFloat(lonlat[1]).toFixed(4);
        validateClickPointIsValid()
    });
    map.getLayers().item(1).setZIndex(10000);

    $('#resetPage').on('click', function () {
        var location = window.location;
        location.href = location.origin + location.pathname;
    });

    $('#years').select2();
    $('.btn-plot').addClass('disabled');
});