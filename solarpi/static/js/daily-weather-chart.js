$(document).ready(function () {
    $(function () {
        $('#daily-weather-chart').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Temperature'
            },
            colors: ['#153E7E', '#B4C7DA', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                min: 0,
                title: {
                    text: '°C'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} °C</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0,
                    pointWidth: 3
                }
            },
            series: [
                {
                    name: 'Temperature',
                    data: data
                },
            ]
        });
    });
});
    