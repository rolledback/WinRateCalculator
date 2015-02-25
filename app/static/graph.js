window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        exportEnabled: true,
        border:true,
        axisY:{
            title: "Win Rate",
            titleFontSize: 22,
            includeZero: false,
            labelFontSize: 14,
            interlacedColor: "#F0F8FF"
        },
        legend:{
            horizontalAlign: "center"
        },
        axisX:{
            labelFontSize: 14
        },
        data: [{
            type: "line",
            showInLegend: "true",
            legendText: "Battles",
            dataPoints: data
        }]
    });
    chart.render();
}

