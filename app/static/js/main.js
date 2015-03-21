var controllers = angular.module('controllers', []);

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


controllers.controller('CalcCtrl', ['$scope', '$log', '$http', '$location',
    function($scope, $log, $http) {
        $scope.init_calc = function() {
            var qbattles = $location.search()['battles'];
            var qwins = $location.search()['wins'];
            var qcurr_rate = $location.search()['curr'];
            var qnew_rate = $location.search()['new'];
            var qgoal_rate = $location.search()['goal'];

            $http.get('api/calc?battles=' + qbattles + '&wins=' + qwins + '&curr=' + qcurr_rate + '&new=' + qnew_rate + '&goal=' + qgoal_rate).
                success(function(results) {
                    $scope.data_points = angular.toJson(results['data_points']);
                    $scope.new_rate = results['new_rate'];
                    $scope.orig_rate = results['orig_rate'];
                    $scope.new_wins = results['new_wins'];
                    $scope.new_losses = results['new_losses'];
                    $scope.new_battles = results['new_battles'];
                    $scope.goal_rate = results['goal_rate'];
                    $scope.nick = results['nick'];
                });
        };
        $scope.init_calc();
    }
]);


controllers.controller('PlayerCtrl', ['$scope', '$log', '$http', '$routeParams','$location',
    function($scope, $log, $http, $routeParams, $location) {
        $scope.init_player = function($q) {
            $log.log('inside init player');
            var deferred = $q.defer()
            $http.get('api/player/' + $routeParams.name).
                success(function(results) {
                    $scope.tanks = results['tanks'];
                    $scope.name = results['name'];
                });
            return deferred.promise;
        };
        //$scope.init_player();
/*
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
        });*/
    }
]);

