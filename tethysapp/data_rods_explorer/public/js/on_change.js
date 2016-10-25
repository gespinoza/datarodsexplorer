function oc_model() {
    var GLDASFlashMessageID = 'GLDAS-get-map-disabled';
    var GLDASFlashMessageText = 'GLDAS does not support the "Display Map" function, ' +
        'but data rods data can still be obtained under the "Plot one variable" or "Compare two variables" options.';
    var href;
    var GET = getUrlVars();
    var model = $('#model1').val();
    var btnDisplayMap = $('#btnDisplayMap');

    // All datepickers (plotTime, startDate`, endDate), the model and variable are affected by this change event. Everything else stays the same.
    updateFences('1', model); // The "1" refers to "Model 1". Thus Model 1's fences will be updated.
    GET['model'] = model;
    GET['variable'] = VAR_DICT[model][0].value; //1st element
    GET['plotTime'] = dateHourPickerToRodsDate($('#plot_date').val(), $('#plot_hour').val());

    if ($('#endDate1').val()) {
        GET['endDate'] = dateHourPickerToRodsDate($('#endDate1').val(), '23');
    }

    if ($('#startDate1').val()) {
        GET['startDate'] = dateHourPickerToRodsDate($('#startDate1').val(), '00');
    }

    href = constructHref(GET);
    history.pushState("", "", href);
    loadVariableOptions('model', 'variable');
    if (model === "GLDAS") {
        btnDisplayMap.prop('disabled', true);
        displayFlashMessage(GLDASFlashMessageID, 'info', GLDASFlashMessageText)
    } else {
        btnDisplayMap.prop('disabled', false);
        removeFlashMessage(GLDASFlashMessageID)
    }
}

function oc_variable() {
    var href;
    var GET = getUrlVars();

    // Only the variable is affected by this change event. Everything else stays the same.
    GET['variable'] = $('#variable').val();

    href = constructHref(GET);
    history.pushState("", "", href);
}

function oc_map_dt() {
    var href;
    var GET = getUrlVars();

    // Only the plotTime is affected by this change event. Everything else stays the same.
    GET['plotTime'] = dateHourPickerToRodsDate($('#plot_date').val(), $('#plot_hour').val());

    href = constructHref(GET);
    history.pushState("", "", href);
}

function oc_sten_dt(datePickerID) {
    var href;
    var GET = getUrlVars();
    var differentiator = datePickerID[datePickerID.length - 1];
    var $startDate = $('#startDate' + differentiator);
    var $endDate = $('#endDate' + differentiator);

    // Always have both startDates (model 1 and 2) and both endDates (model 1 and 2) match
    $('.' + datePickerID.slice(0, -1)).val($('#' + datePickerID).val());


    GET['startDate'] = dateHourPickerToRodsDate($startDate.val(), '00'); //First hour
    GET['endDate'] = dateHourPickerToRodsDate($endDate.val(), '23'); //Last hour

    href = constructHref(GET);
    history.pushState("", "", href);

    if (datePickerID.indexOf('endDate') !== -1) {
        $startDate.datepicker('setEndDate', $('#' + datePickerID).val());
    }
}

function oc_model2() {
    var href;
    var GET = getUrlVars();
    var model2 = $('#model2').val();

    updateFences('2', model2);
    GET['model2'] = model2;
    GET['variable2'] = VAR_DICT[model2][0].value; //1st element
    var endDate = dateHourPickerToRodsDate($('#endDate2').val(), '23');
    var startDate = dateHourPickerToRodsDate($('#startDate2').val(), '00');

    GET['endDate'] = endDate;
    GET['startDate'] = startDate;

    href = constructHref(GET);
    history.pushState("", "", href);
    loadVariableOptions('model2', 'variable2');
}

function oc_variable2() {
    var href;
    var GET = getUrlVars();

    // Only variable2 is affected by this change event. Everything else stays the same.
    GET['variable2'] = $('#variable2').val();

    href = constructHref(GET);
    history.pushState("", "", href);
}

function oc_years() {
    var href;
    var GET = getUrlVars();

    //From here the code is new
    var yearsList = $('#years').val();

    if (yearsList && yearsList.length > 0) {
        GET['years'] = yearsList.join(',');
    }

    href = constructHref(GET);
    history.pushState("", "", href)
}
