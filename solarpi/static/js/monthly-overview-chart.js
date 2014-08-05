$(function () {
    $('#monthly-overview-chart').highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Energy Production for 2014'
        },
        colors: ['#428BCA', '#153E7E', '#B4C7DA', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        xAxis: [
            {
                type: 'datetime',
                dateTimeLabelFormats: {
                    month: '%b',
                    year: '%b'
                }
            }
        ],
        yAxis: [
            { // Primary yAxis
                labels: {
                    format: '{value} kWh',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Energy',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }
        ],
        tooltip: {
            shared: true,
            headerFormat: '<b>{point.x: %B}</b><br>',
            pointFormat: '{series.name}: {point.y:.2f} kWh<br>'
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
                    valueSuffix: ' kWh'
                }

            },
            {
                name: '2013',
                type: 'line',
                yAxis: 0,
                data: series_2013,
                tooltip: {
                    valueSuffix: ' kWh'
                }
            }
        ]
    });
});