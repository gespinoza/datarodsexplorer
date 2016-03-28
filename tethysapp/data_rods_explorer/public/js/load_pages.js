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
}

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
	}
}
