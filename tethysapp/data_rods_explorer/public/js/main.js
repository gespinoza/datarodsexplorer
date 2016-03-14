function load_default_home() {
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
		var plotTime = date_to_normal(current_date(140));
	    document.getElementById('plot_date').value = plotTime['date'];
	    document.getElementById('plot_hour').value = plotTime['hour'];
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
}

function load_default_plot() {
	var counter = 0;
	var GET = getUrlVars();
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
		document.getElementById('model').value = model;
		document.getElementById('variable').value = varia;
		document.getElementById('plot_date').value = plotTime['date'];
		document.getElementById('plot_hour').value = plotTime['hour'];
		document.getElementById('startDate').value = startDate['date'];
	    document.getElementById('endDate').value = endDate['date'];
	}
}

function load_default_plot2() {
	var counter = 0;
	var GET = getUrlVars();
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

function load_default_years() {
	var counter = 0;
	var GET = getUrlVars();
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
		/*
		if (years.indexOf(',') === -1) {
			document.getElementById('years').value = years;
		} else {
			var years_options = document.getElementById('years');
			var years_list = years.split(',');
			for (var i=0; i < years_options.length; i++) {
				if (years_list.indexOf(years_options[i].value) != -1) {
					years_options[i].selected = true;
				}
			}
		}
		*/
	}
}

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

function oc_model() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = document.getElementById('model').value;
	var varia = VAR_DICT[model][0].value; //1st element
	var plotDate = GET['plotTime'];
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
	if (GET['model2'] && GET['variable2']) {
		var model2 = GET['model2'];
		var varia2 = GET['variable2'];
		href = href + '&model2=' + model2 + '&variable2=' + varia2;
	}
	if (GET['startDate'] && GET['endDate']) {
		var startDate = GET['startDate'];
		var endDate = GET['endDate'];
		href = href + '&startDate=' + startDate + '&endDate=' + endDate;
	}
	if (GET['years']) {
		var years = GET['years'];
		href = href + '&years=' + years;
	}
	history.pushState("", "", href);
	load_variable_options('model', 'variable');
}

function oc_variable() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model'];
	var varia = document.getElementById('variable').value;
	var plotDate = GET['plotTime'];
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
	if (GET['model2'] && GET['variable2']) {
		var model2 = GET['model2'];
		var varia2 = GET['variable2'];
		href = href + '&model2=' + model2 + '&variable2=' + varia2;
	}
	if (GET['startDate'] && GET['endDate']) {
		var startDate = GET['startDate'];
		var endDate = GET['endDate'];
		href = href + '&startDate=' + startDate + '&endDate=' + endDate;
	}
	if (GET['years']) {
		var years = GET['years'];
		href = href + '&years=' + years;
	}
	history.pushState("", "", href);
}

function oc_map_dt() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model'];
	var varia = GET['variable'];
	var plot_date = date_to_rods(document.getElementById('plot_date').value);
	var plot_hour = document.getElementById('plot_hour').value;
	var plotDate = plot_date + 'T' + plot_hour;
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
	if (GET['model2'] && GET['variable2']) {
		var model2 = GET['model2'];
		var varia2 = GET['variable2'];
		href = href + '&model2=' + model2 + '&variable2=' + varia2;
	}
	if (GET['startDate'] && GET['endDate']) {
		var startDate = GET['startDate'];
		var endDate = GET['endDate'];
		href = href + '&startDate=' + startDate + '&endDate=' + endDate;
	}
	history.pushState("", "", href);
}

function oc_sten_dt() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model'];
	var plotDate = GET['plotTime'];
	var varia = GET['variable'];
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;
	if (GET['model2'] && GET['variable2']) {
		var model2 = GET['model2'];
		var varia2 = GET['variable2'];
		href = href + '&model2=' + model2 + '&variable2=' + varia2;
	}
	var startDate = date_to_rods(document.getElementById('startDate').value) + 'T00'; //First hour
	var endDate = date_to_rods(document.getElementById('endDate').value) + 'T23'; //Last hour
	href = href  + '&startDate=' + startDate + '&endDate=' + endDate;
	history.pushState("", "", href);
}

function oc_model2() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model']; //document.getElementById('model').value;
	var varia = GET['variable']; //document.getElementById('variable').value;
	var plotDate = GET['plotTime'];
	var startDate = GET['startDate'];//date_to_rods(document.getElementById('startDate').value) + 'T00'; //First hour
	var endDate = GET['endDate'];//date_to_rods(document.getElementById('endDate').value) + 'T23'; //Last hour
	var model2 = document.getElementById('model2').value;
	var varia2 = VAR_DICT[model2][0].value; //1st element
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate + '&model2=' + model2 + '&variable2=' + varia2 + '&startDate=' + startDate + '&endDate=' + endDate;
	history.pushState("", "", href);
	load_variable_options('model2', 'variable2');
}

function oc_variable2() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model']; //document.getElementById('model').value;
	var varia = GET['variable']; //document.getElementById('variable').value;
	var plotDate = GET['plotTime'];
	var startDate = GET['startDate'];//date_to_rods(document.getElementById('startDate').value) + 'T00'; //First hour
	var endDate = GET['endDate'];//date_to_rods(document.getElementById('endDate').value) + 'T23'; //Last hour
	var model2 = GET['model2'];
	var varia2 = document.getElementById('variable2').value;
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate + '&model2=' + model2 + '&variable2=' + varia2 + '&startDate=' + startDate + '&endDate=' + endDate;
	history.pushState("", "", href);
}

function oc_years() {
	var GET = getUrlVars();
	var href = window.location.href.split('?')[0];
	var model = GET['model']; //document.getElementById('model').value;
	var varia = GET['variable']; //document.getElementById('variable').value;
	var plotDate = GET['plotTime'];
	//From here the code is new
	var yearsDoc = document.getElementById('years').selectedOptions;
	var yearsObj = [];
	for (var i=0; i<yearsDoc.length; i++) {
		yearsObj = yearsObj.concat(yearsDoc[i].value);
	}
	yearsObj = getRanges(yearsObj);
	var years = "";
	for (var i=0; i<yearsObj.length; i++) {
		years = years + yearsObj[i] + ',';
	}
	years = years.substr(0, years.length - 1)
	/*
	var yearsObj = document.getElementById('years').selectedOptions;
	var years = "";
	for (var i=0; i<yearsObj.length; i++) {
		years = years + yearsObj[i].value + ',';
	}
	years = years.substr(0, years.length - 1)
	*/
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate + '&years=' + years;
	history.pushState("", "", href)
}
/*
function check_get_href() {
	var href = window.location.href;
	var ix = href.indexOf("?");
	if (ix != -1) {
		href = window.location.href.split('?')[0];
	}
	return href;
}
*/
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

function page_and_parameters_html(href, page) {
	var GET = getUrlVars();
	var href = href + '?';
	for (var key in GET) {
		href = href + '&' + key + '=' + GET[key];
	}
	page_and_parameters(href, page);
}

function page_and_parameters(href, page) {
	var GET = getUrlVars(href);
	href = href.split('?')[0]
	if (GET['model']) {
		var model = GET['model'];
	} else {
		var model = document.getElementById('model').value;
	}
	if (GET['variable']) {
		var varia = GET['variable'];
	} else {
		var varia = VAR_DICT[model][0].value;//document.getElementById('variable').value;
	}
	if (GET['plotTime']) {
		var plotDate = GET['plotTime'];
	} else {
		var plotTime = date_to_normal(current_date(140));
	    var plotDate = date_to_rods(plotTime['date']) + 'T' + plotTime['hour'];
	}
	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate;

	if (page == 'plot') {
		if (GET['endDate']) {
			endDate = GET['endDate'];
		} else {
			var endDate = current_date(133, '23');
		}
		if (GET['startDate']) {
			startDate =  GET['startDate'];
		} else {
			var startDate = current_date(140, '0');
		}
		href = href + '&startDate=' + startDate + '&endDate=' + endDate;
	} else if (page == 'plot2') {
		if (GET['model2']) {
			var model2 = GET['model2'];
		} else {
			var model2 = 'nldas'; //1st element
		}
		if (model === model2 && varia == VAR_DICT[model][0].value) {
			var varia2 = VAR_DICT[model2][1].value;
		} else {
			var varia2 = VAR_DICT[model2][0].value;
		}
		if (GET['endDate']) {
			endDate = GET['endDate'];
		} else {
			var endDate = current_date(133, '23');
		}
		if (GET['startDate']) {
			startDate =  GET['startDate'];
		} else {
			var startDate = current_date(140, '0');
		}
		href = href + '&model2=' + model2 + '&variable2=' + varia2 + '&startDate=' + startDate + '&endDate=' + endDate;
	} else if (page == 'years') {
		var endDate = current_date(140, '23');
		years = endDate.substr(0, 4);
		href =  href + '&years=' + years;
	}
	window.location = href;
	
	/*
	var form = document.createElement("form");
	var input = document.createElement("input");
	var token = document.createElement("token");
	form.method = "POST";
	form.action = href;
	input.name = "store_id";
	input.value = prueba;
	token.name = "csrfmiddlewaretoken";
	token.value = document.cookie.split('csrftoken=')[1];
	form.appendChild(input);
	document.body.appendChild(form);
	form.submit();
	*/
}

/*
function add_get_startDate() {
	var href = window.location.href.split('?')[0];
	var GET = getUrlVars();
	var startDate = date_to_rods(document.getElementById('startDate').value);
	startDate = startDate + 'T00'; //First hour
	var model = GET['model'];
	var varia = GET['variable'];
	href = href + '?model=' + model + '&variable=' + varia + '&startDate=' + startDate;
    if (GET['endDate']) {
      href = href + '&endDate=' + GET['endDate'];
    }
    window.location = href;
}

function add_get_endDate() {
	var href = window.location.href.split('?')[0];
	var GET = getUrlVars();
	var endDate = date_to_rods(document.getElementById('endDate').value);
	endDate = endDate + 'T23'; //Last hour
	var model = GET['model'];
	var varia = GET['variable'];
	var startDate = GET['startDate'];
	href = href + '?model=' + model + '&variable=' + varia;
    if (GET['startDate']) {
      href = href + '&startDate=' + GET['startDate'];
    }
    href = href + '&endDate=' + endDate;
    window.location = href;
}
*/

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
		window.alert(lonlat);
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
	//document.getElementById('plot_btn').value = true;
}

function load_map() {
	document.getElementById('loadMap').value = "no";
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

function two_axis_plot(series, y_axis_1, y_axis_2) {
	series = series.replace(/\&#39;/g, "'")
	series = series.replace(/datetime.datetime/g, "Date.UTC")
	var datarods_ts = eval(series);

	arrayLength = datarods_ts[0]['data'].length;
	for (var i = 0; i < arrayLength; i++) {
		var time1 = new Date(datarods_ts[0]['data'][i][0]);
		var time2 = new Date(datarods_ts[1]['data'][i][0]);
		datarods_ts[0]['data'][i][0] = time1.setMonth(time1.getMonth() - 1);
	    datarods_ts[1]['data'][i][0] = time2.setMonth(time2.getMonth() - 1);
	    }

    $('#plot2container').highcharts({
        chart: {
            type: 'line',
        },
        title: {
            text: '',
            style: {
            	display: 'none'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
        },
        yAxis: [{
            lineWidth: 1,
            title: {
                text: datarods_ts[0].code
            }
        }, {
            lineWidth: 1,
            opposite: true,
            title: {
                text: datarods_ts[1].code
            }
        }],
        
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        legend: {
        	enabled: true,
        },
        series: [{
            name: datarods_ts[0].name,
            data: datarods_ts[0].data,
            yAxis: 0
        }, {
            name: datarods_ts[1].name,
            data: datarods_ts[1].data,
            yAxis: 1
        }]
    });
};


var VAR_DICT = new Object();
VAR_DICT["nldas"] = [
						{"text": "Precipitation hourly total (kg/m^2)",
						"value": "APCPsfc"},
						{"text": "Surface DW longwave radiation flux (W/m^2)",
						"value": "DLWRFsfc"},
						{"text": "Surface DW shortwave radiation flux (W/m^2)",
						"value": "DSWRFsfc"},
						//{"text": "Potential evaporation (kg/m^2)",
						//"value": "PEVAPsfc"},
						{"text": "2-m above ground specific humidity (kg/kg)",
						"value": "SPFH2m"},
						{"text": "2-m above ground temperature (K)",
						"value": "TMP2m"},
						//{"text": "10-m above ground zonal wind (m/s)",
						//"value": "UGRD10m"},
						//{"text": "10-m above ground meridional wind (m/s)",
						//"value": "VGRD10m"},
						{"text": "Total evapotranspiration (kg/m^2)",
						"value": "EVPsfc"},
						{"text": "Ground heat flux (w/m^2)",
						"value": "GFLUXsfc"},
						{"text": "Latent heat flux (w/m^2)",
						"value": "LHTFLsfc"},
						{"text": "Sensible heat flux (w/m^2)",
						"value": "SHTFLsfc"},
						{"text": "Surface runoff (non-infiltrating) (kg/m^2)",
						"value": "SSRUNsfc"},
						//{"text": "Subsurface runoff (baseflow) (kg/m^2)",
						//"value": "BGRIUNdfc"},
						{"text": "0-10 cm soil moisture content (kg/m^2)",
						"value": "SOILM0-10cm"},
						{"text": "0-100 cm soil moisture content (kg/m^2)",
						"value": "SOILM0-100cm"},
						{"text": "0-200 cm soil moisture content (kg/m^2)",
						"value": "SOILM0-200cm"},
						{"text": "10-40 cm soil moisture content (kg/m^2)",
						"value": "SOILM10-40cm"},
						{"text": "40-100 cm soil moisture content (kg/m^2)",
						"value": "SOILM40-100cm"},
						{"text": "100-200 cm soil moisture content (kg/m^2)",
						"value": "SOILM100-200cm"},
						{"text": "0-10 cm soil temperature (K)",
						"value": "TSOIL0-10cm"}
				   ];
VAR_DICT["gldas"] = [
						{"text": "Total Evapotranspiration (kg/m^2/s)",
						"value": "Evap"},
						{"text": "Precipitation rate (kg/m^s/hr)",
						"value": "precip"},
						{"text": "Rain rate (kg/m^2/s)",
						"value": "Rainf"},
						{"text": "Snow rate (kg/m^2/s)",
						"value": "Snowf"},
						{"text": "Surface Runoff (kg/m^2/s)",
						"value": "Qs"},
						{"text": "Subsurface Runoff (kg/m^2/s)",
						"value": "Qsb"},
						{"text": "0-100 cm top 1 meter soil moisture content (kg/m^2)",
						"value": "SOILM0-100cm"},
						{"text": "0-10 cm layer 1 soil moisture content (kg/m^2)",
						"value": "SOILM0-10cm"},
						{"text": "10-40 cm layer 2 soil moisture content (kg/m^2)",
						"value": "SOILM10-40cm"},
						{"text": "40-100 cm layer 3 soil moisture content (kg/m^2)",
						"value": "SOILM40-100cm"},
						{"text": "Near surface air temperature (K)",
						"value": "Tair"},
						{"text": "Average layer 1 soil temperature (K)",
						"value": "TSOIL0-10cm"},
						{"text": "Near surface wind magnitude (m/s)",
						"value": "Wind"}
				   ];
VAR_DICT["trmm"] = [
			           {"text": "Precipitation (mm/hr)",
			            "value": "precip"}
				   ];

VAR_DICT["grace"] = [
			           {"text": "Surface Soil Moisture Percentile",
			            "value": "surf"}, 
			           {"text": "Root Zone Soil Moisture Percentile",
			            "value": "root"},
			           {"text": "Ground Water Percentile",
			       		"value": "deep"}
				   ];

