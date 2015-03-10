app = angular.module("manager-app");

app.factory("Profile", ['$http', 'info', function ($http, info) {

    function Profile(data) {
        this.username = data.username;
        this.email = data.email;
    }

    return Profile;
}]);