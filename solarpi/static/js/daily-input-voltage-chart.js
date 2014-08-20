$(document).ready(function () {
    $(function () {
        $('#daily-input-voltage-chart').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Input Voltage'
            },
            colors: ['#B4C7DA', '#153E7E', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Volt'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} Volt</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                series: {
                    marker: {
                        radius: 2
                    }
                }
            },
            series: [
                {
                    name: 'String 1',
                    data: input_voltage_1
                },
                {
                    name: 'String 2',
                    data: input_voltage_2
                }
            ]
        });
    });
});
    