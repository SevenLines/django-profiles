/**
 * Created by m on 08.03.15.
 */

app = angular.module("manager-app");

app.controller("ProfilesCtrl", ['$scope', '$http', 'info', function ($scope, $http, info) {
    $scope.info = info;

    $http.get(commonUrls.profiles).success(function (data) {
        $scope.profiles = data.objects;
    });

    $scope.setActiveProfile = function (profile) {
        $scope.info.profile = profile;
    }
}]);

