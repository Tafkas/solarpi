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
                categories: ['Apr', 'May', 'Jun', 'Jul', 'Aug']
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
            },
            { // Secondary yAxis
                title: {
                    text: 'Power',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value} kW',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                opposite: true
            }
        ],
        tooltip: {
            shared: true
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
                yAxis: 1,
                data: series,
                tooltip: {
                    valueSuffix: ' kW'
                }

            }
        ]
    });
});