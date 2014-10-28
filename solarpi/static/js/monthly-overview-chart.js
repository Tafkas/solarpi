$(function () {
    $('#monthly-overview-chart').highcharts({
        chart: {

        },
        title: {
            text: 'Energy Output for 2014'
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
            y: 100,
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