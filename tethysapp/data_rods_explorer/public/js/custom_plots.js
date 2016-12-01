function two_axis_plot(series) {
    series = series.replace(/&#39;/g, "'");
    series = series.replace(/datetime.datetime/g, "Date.UTC");
    series = series.replace(/, tzinfo=tzlocal\(\)/g, "");
    var datarods_ts = eval(series);

    var array1Length = datarods_ts[0]['data'].length;

    for (var i = 0; i < array1Length; i++) {
        var time1 = new Date(datarods_ts[0]['data'][i][0]);
        datarods_ts[0]['data'][i][0] = time1.setMonth(time1.getMonth() - 1);
    }

    var array2Length = datarods_ts[1]['data'].length;

    for (var j = 0; j < array2Length; j++) {
        var time2 = new Date(datarods_ts[1]['data'][j][0]);
        datarods_ts[1]['data'][j][0] = time2.setMonth(time2.getMonth() - 1);
    }

    $('#plot2container').highcharts({
        chart: {
            type: 'line'
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
                month: '%e. %b'
            }
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
            pointFormat: '{point.x:%e. %b}: {point.y:.2f}'
        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        legend: {
            enabled: true
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
}
