$(function() {
    var map = TETHYS_MAP_VIEW.getMap();
    map.on('singleclick', function(evt) {
        var pointSource = map.getLayers().item(1).getSource();

        while (pointSource.getFeatures().length > 1) {
            pointSource.removeFeature(pointSource.getFeatures()[0]);
        }

        var coords = evt.coordinate;
        var lonlat = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
        document.getElementById('pointLonLat').value = parseFloat(lonlat[0]).toFixed(4) + ',' + parseFloat(lonlat[1]).toFixed(4);
        removeFlashMessage('no-query-location');
        removeFlashMessage('point-out-extents');
        removeFlashMessage('error999');
        removeFlashMessage('out-of-bouds');
        if (pointIsOutOfBounds(lonlat, $('#model').val(), $('#model2').val())) {
            displayFlashMessage('warning', 'Query location outside of model extents. Please choose a new location.');
            $('a[name*=plot]').add('a[name=years]').addClass('disabled');
        } else {
            $('a[name*=plot]').add('a[name=years]').removeClass('disabled');
        }
    });
    map.getLayers().item(1).setZIndex(10000);
});