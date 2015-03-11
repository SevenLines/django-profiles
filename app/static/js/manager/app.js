/**
 * Created by m on 07.03.15.
 */


app = angular.module("manager-app", []);

// shared data factory
app.factory("info", function () {
    var self = this;
    self.profile = null; // current active profile
    self.user = null;  // current active  user

    self.gen_password = function (length) {
        var charset = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            retVal = "";
        for (var i = 0, n = charset.length; i < length; ++i) {
            retVal += charset.charAt(Math.floor(Math.random() * n));
        }
        return retVal;
    };

    return this;
});


