var wotApp = angular.module('WoTApp', ['ngRoute', 'controllers']);
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
            resolve: angular.module('controllers').controller('PlayerCtrl').init_player
        })
        .when('/calc', {
            templateUrl: '/static/views/result.html',
            controller: 'CalcCtrl'
        })
        .when('/about', {
            templateUrl: '/static/views/about.html',
            controller: 'AboutCtrl'
        })
        .otherwise({
            redirectTo: '/home'
        });
    }]);
