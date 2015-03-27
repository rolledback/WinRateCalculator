var wotApp = angular.module('WoTApp', ['ngRoute']);
wotApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider
        .when('/home', {
            templateUrl: '/static/views/index.html',
            controller: 'IndexCtrl'
        })
        .when('/player/:name', {
            templateUrl: '/static/views/player.html',
            controller: 'PlayerCtrl',
            resolve: {
                "playerResults": function($q, $http, $route) {
                    var playerAPI = $q.defer();
                    $http.get('api/player/' + $route.current.params.name).
                        success(function(results) {
                        playerAPI.resolve({
                            tanks: function() {
                                return results['tanks'];
                            },
                            name:  function() {
                                return results['name'];
                            }
                        });
                    });
                    return playerAPI.promise;
                }
            }
        })
        .when('/calc', {
            templateUrl: '/static/views/result.html',
            controller: 'CalcCtrl',
            resolve: {
                "calcResults": function($q, $http, $location, $log) {
                    var qbattles = $location.search()['battles'];
                    var qwins = $location.search()['wins'];
                    var qcurr_rate = $location.search()['curr'];
                    var qnew_rate = $location.search()['new'];
                    var qgoal_rate = $location.search()['goal'];
                    var qnick = $location.search()['nick'];

                    var calcAPI = $q.defer();
                    var queryURL = '';
                    if(qnick)
                        queryURL = 'api/calc?battles=' + qbattles + '&wins=' + qwins + '&curr=' + qcurr_rate + '&new=' + qnew_rate + '&goal=' + qgoal_rate + '&nick=' + qnick;
                    else
                        queryURL = 'api/calc?battles=' + qbattles + '&wins=' + qwins + '&curr=' + qcurr_rate + '&new=' + qnew_rate + '&goal=' + qgoal_rate;

                    $http.get(queryURL).
                        success(function(results) {
                        calcAPI.resolve({
                            result: function() {
                                return results;
                            }
                        });
                    });
                    return calcAPI.promise;
                }
            }
        })
        .when('/about', {
            templateUrl: '/static/views/about.html',
            controller: 'AboutCtrl'
        })
        .otherwise({
            redirectTo: '/home'
        });
    }]);
