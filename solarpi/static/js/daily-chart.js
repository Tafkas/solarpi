$(document).ready(function () {
    $(function () {
        $('#daily-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Power generation'
            },
            colors: ['#B4C7DA', '#153E7E', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Watt'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} Watt</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.0,
                    groupPadding: 0.5,
                    borderWidth: 0,
                    pointWidth: 5
                }
            },
            series: [
                {
                    name: 'Max Power Output ± 3 Days',
                    data: data_max
                },
                {
                    name: 'Power Output',
                    data: data
                }
            ]
        });
    });
});
    