var controllers = angular.module('WoTApp');

var tanks = [];
var name = '';
var data_points = [];

controllers.controller('IndexCtrl', ['$scope', '$log', '$http',
    function($scope, $log, $http) {}
]);

controllers.controller('AboutCtrl', ['$scope', '$log', '$http',
    function($scope, $log, $http) {}
]);

controllers.controller('MainCtrl', ['$scope', '$log', '$http', '$location',
    function($scope, $log, $http, $location) {
        $scope.search = function(playerName) {
            $log.log(playerName);
            $location.path('/player/' + playerName);
        };
    }
]);


controllers.controller('CalcCtrl',
    function($scope, calcResults, $log) {
        $scope.data_points = calcResults.result()['data_points'];
        $scope.new_rate = calcResults.result()['new_rate'];
        $scope.orig_rate = calcResults.result()['orig_rate'];
        $scope.new_wins = calcResults.result()['new_wins'];
        $scope.new_losses = calcResults.result()['new_losses'];
        $scope.new_battles = calcResults.result()['new_battles'];
        $scope.goal_rate = calcResults.result()['goal_rate'];
        $scope.nick = calcResults.result()['nick'];

        $scope.chart = new CanvasJS.Chart("chartContainer", {
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
                dataPoints: $scope.data_points,
            }]
        });
        $scope.chart.render();
    }
);


controllers.controller('PlayerCtrl',
    function($scope, playerResults) {
        $scope.tanks = playerResults.tanks();
        $scope.name = playerResults.name();
    }
);

