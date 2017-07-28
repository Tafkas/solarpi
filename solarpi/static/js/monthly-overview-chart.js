$(function () {
    $('#monthly-overview-chart').highcharts({
        chart: {},
        title: {
            text: 'Energy Output for ' + new Date().getFullYear()
        },
        colors: ['#B4C7DA', '#428BCA', '#153E7E', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        xAxis: [
            {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            }
        ],
        yAxis: [
            {
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
            headerFormat: '<b>{point.x}</b><br>',
            pointFormat: '{series.name}: {point.y} <br>'
        },
        plotOptions: {
            column: {
                pointPadding: 0.0,
                groupPadding: 0.5,
                borderWidth: 0,
                pointWidth: 30
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 40,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [
            {
                name: 'Prediction',
                type: 'column',
                data: current_month_pred,
                tooltip: {
                    valueSuffix: ' kWh',
                    formatter: function () {
                        if (this.y != null) {
                            return this.y;
                        }
                        else return false;
                    }
                }
            },
            {
                name: new Date().getFullYear(),
                type: 'column',
                yAxis: 0,
                data: current_year_series,
                tooltip: {
                    valueSuffix: ' kWh'
                }

            },
            {
                name: 'Last years average',
                type: 'line',
                yAxis: 0,
                data: average_years_series,
                tooltip: {
                    valueSuffix: ' kWh'
                }
            },
            {
                name: 'Last years min max',
                type: 'errorbar',
                data: min_max_years_series,
                tooltip: {
                    pointFormat: '(Previous years\' range: {point.low}-{point.high} kWh)<br/>'
                }
            }
        ]
    });
});