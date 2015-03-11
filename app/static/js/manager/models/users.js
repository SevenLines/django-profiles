/**
 * Created by m on 07.03.15.
 */


app = angular.module("manager-app");

// shared data factory
app.factory("Users", ['$http', 'User', function ($http, User) {
    var self = this;
    $http.get(commonUrls.profilepasskeys).success(function (data) {
        var profile_passkeys = data.objects;

        $http.get(commonUrls.users).success(function (data) {
            self.list = data.objects.map(function (item) {
                return new User(item, profile_passkeys)
            });
        });
    });

    return this;
}]);


