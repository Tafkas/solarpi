$(document).ready(function () {
    $(function () {
        $('#monthly-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Daily Energy Output'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'p in kW'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:&nbsp; </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} kW</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [
                {
                    name: 'Daily Energy Output',
                    data: data
                }
            ]
        });
    });
});
