window.onload = function () {
   var chart = new CanvasJS.Chart("chartContainer", {
       theme: "theme2",
       animationEnabled: true,
       axisY:{
           includeZero: false 
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

