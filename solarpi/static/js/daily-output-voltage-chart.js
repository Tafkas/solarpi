$(document).ready(function () {
    $(function () {
        $('#daily-output-voltage-chart').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Output Voltage'
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
                    name: 'L1',
                    data: output_voltage_1
                },
                {
                    name: 'L2',
                    data: output_voltage_2
                },
                {
                    name: 'L3',
                    data: output_voltage_3
                }
            ]
        });
    });
});
    