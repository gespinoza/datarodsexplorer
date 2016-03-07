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
		var lonlat = ol.proj.transform(map.getEventCoordinate(evt), 'EPSG:3857', 'EPSG:4326');
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
	var center = ol.proj.toLonLat(view.getCenter())
	document.getElementById('lonW').value = topleft[0];
	document.getElementById('latS').value = bottomright[1];
	document.getElementById('lonE').value = bottomright[0];
	document.getElementById('latN').value = topleft[1];
	document.getElementById('zoom').value = zoom;
	document.getElementById('centerX').value = center[0];
	document.getElementById('centerY').value = center[1];
}

function load_map() {
	load_map_post_parameters();
	document.getElementById('retrieveMap').value = "yes";
	document.forms['parametersForm'].submit();
}

function createPlot() {
	load_map_post_parameters();
	document.getElementById('retrieveMap').value = "no";
	document.getElementById('prevPlot').value = "yes";
	document.forms['parametersForm'].submit();
}

