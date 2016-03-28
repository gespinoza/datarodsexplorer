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

	href = href + '?model=' + model + '&variable=' + varia + '&plotTime=' + plotDate + '&years=' + years;
	history.pushState("", "", href)
}
