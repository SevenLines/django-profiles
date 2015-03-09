/**
 * Created by m on 08.03.15.
 */

app = angular.module("manager-app");

app.controller("UsersCtrl", ['$scope', '$http', 'info', 'User', function ($scope, $http, info, User) {
    $scope.info = info;
    $http.get(commonUrls.profilepasskeys).success(function (data) {
        var profile_passkeys = data.objects;

        $http.get(commonUrls.users).success(function (data) {
            $scope.users = data.objects.map(function (item) {
                return new User(item, profile_passkeys)
            });
        });
    });

    $scope.setActiveUser = function (user) {
        /***
         * set active user in global info object
         */
        $scope.info.user = user;
    };

    $scope.save = function () {
        /***
         * saves all changed users passkeys
         * @type {Array}
         */
        var data_to_send = [];
        $scope.users.forEach(function (item) {
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
            $scope.users.forEach(function (item) {
                item.reset();
            });
        });
    };
}]);
