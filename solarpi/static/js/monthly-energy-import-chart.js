$(document).ready(function () {
    $(function () {
        $('#monthly-import-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Last 30 Days Energy Import'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'w in kWh'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:&nbsp; </td>' +
                '<td style="padding:0"><b>{point.y:.1f} kWh</b></td></tr>',
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
                    name: 'Daily Energy Import',
                    data: importData
                }
            ]
        });
    });
});
