$(document).ready(function () {
    $(function () {
        $('#yearly-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Yearly Energy Output'
            },
            colors: ['#428BCA', '#153E7E', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            xAxis: {
                categories: years
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
                    name: 'Yearly Energy Output',
                    data: data
                },
                {
                    type: 'line',
                    name: 'Estimated Energy Output',
                    data: yearlyData
                }
            ]
        });
    });
});
