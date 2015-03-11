/**
 * Created by m on 08.03.15.
 */

app = angular.module("manager-app");

app.controller("UsersCtrl", ['$scope', '$http', 'info', 'Users', function ($scope, $http, info, users) {
    $scope.info = info;
    $scope.users = users;


    $scope.setActiveUser = function (user) {
        /***
         * set active user in global info object
         */
        info.user = user;
    };

    $scope.save = function () {
        /***
         * saves all changed users passkeys
         * @type {Array}
         */
        var data_to_send = [];
        users.list.forEach(function (item) {
            if (item.changed()) {
                data_to_send.push(item.post_data());
            }
        });
        $http({
            method: "POST",
            url: commonUrls.update_profiles_passkeys,
            data: $.param({
                "profile_passkeys": JSON.stringify(data_to_send),
                "csrfmiddlewaretoken": $.cookie("csrftoken")
            }),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function () {
            users.list.forEach(function (item) {
                item.reset();
            });
        });
    };
    $scope.saveAllowedProfiles = function () {
        var data_to_send = [];
        users.list.forEach(function (item) {
            if (item.profiles_changed()) {
                data_to_send.push(item.post_allowed_profile_data());
            }
        });
        $http({
            method: "POST",
            url: commonUrls.update_allowed_profiles,
            data: $.param({
                "admins": JSON.stringify(data_to_send),
                "csrfmiddlewaretoken": $.cookie("csrftoken")
            }),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function () {
            users.list.forEach(function (item) {
                item.reset_profiles();
            });
        });
    }
}]);
