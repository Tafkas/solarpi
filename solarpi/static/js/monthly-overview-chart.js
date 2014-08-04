$(function () {
    $('#monthly-overview-chart').highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Energy Production for 2014'
        },
        xAxis: [
            {
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    month: '%e. %b',
                    year: '%b'
                }
            }
        ],
        yAxis: [
            { // Primary yAxis
                labels: {
                    format: '{value} kW',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Power',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }
        ],
        tooltip: {
            shared: true,
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x: %b}: {point.y:.2f} kW'
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [
            {
                name: '2014',
                type: 'column',
                yAxis: 0,
                data: series_2014,
                tooltip: {
                    valueSuffix: ' kW'
                }

            },
            {
                name: '2013',
                type: 'line',
                yAxis: 0,
                data: series_2013,
                tooltip: {
                    valueSuffix: ' kW'
                }
            }
        ]
    });
});