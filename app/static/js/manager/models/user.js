/**
 * Created by m on 08.03.15.
 */

app = angular.module("manager-app");

app.factory("User", ['$http', 'info', function ($http, info) {
    /**
     * user model with methods to
     * @param data
     * @param profile_passkeys
     * @constructor
     */
    function User(data, profile_passkeys) {
        var self = this;
        self.id = data.user.id;
        self.username = data.user.username;
        self.email = data.user.email;
        self.is_admin = data.is_admin;
        self.passkeys = {};
        self.allowed = {};

        // map profiles values returned by api
        self.profiles = {};
        data.profiles.forEach(function (item) {
            self.profiles[item.id] = true;
        });

        self.sending_email = false;

        for (var i = 0, l = profile_passkeys.length; i < l; ++i) {
            var profile_passkey = profile_passkeys[i];
            if (profile_passkey.user == self.id) {
                self.passkeys[profile_passkey.profile] = profile_passkey.passkey;
                self.allowed[profile_passkey.profile] = true;
            }
        }

        self.base_allowed = _.clone(self.allowed); // array to check for changing
        self.base_passkeys = _.clone(self.passkeys); // array to check for changing
        self.base_profiles = _.clone(self.profiles); // array to check for changing
    }

    User.prototype = {
        toggleAllowed: function () {
            /***
             * toggle is user allowed to update profile
             */
            if (info.profile) {
                if (!this.allowed[info.profile.id]) {
                    this.allowed[info.profile.id] = true;
                    if (!this.passkeys[info.profile.id]) {
                        this.regenPassword();
                    }
                } else {
                    this.allowed[info.profile.id] = false;
                }
            }
        },
        toggleProfileAllowed: function (profile, allowed) {
            if (this.profiles[profile.id]) {
                this.profiles[profile.id] = false;
            } else {
                this.profiles[profile.id] = true;
            }
        },
        regenPassword: function () {
            /***
             * regend passkey
             */
            if (info.profile) {
                this.passkeys[info.profile.id] = info.gen_password(10);
                this.passkeyChanged();
            }
        },
        changed: function () {
            /***
             * check is object is changed
             */
            for (var item in this.passkeys) {
                if (this.passkeys[item] !== this.base_passkeys[item]) {
                    return true;
                }
            }

            for (var item in this.allowed) {
                if (this.allowed[item] !== this.base_allowed[item]) {
                    return true;
                }
            }
            return false;
        },
        profiles_changed: function () {
            for (var item in this.profiles) {
                if (this.profiles[item] !== this.base_profiles[item]) {
                    return true;
                }
            }
            return false;
        },
        post_data: function () {
            /***
             * returns object suited for  `profiles.views.manager.update_profile_passkeys` view
             */
            return {
                'user': this.id,
                'profile': info.profile.id,
                'passkey': this.passkeys[info.profile.id] ? this.passkeys[info.profile.id] : '',
                'allowed': this.allowed[info.profile.id] ? true : false
            }
        },
        reset: function () {
            /***
             * resets base values, like that object was initially created
             */
            if (!this.allowed[info.profile.id]) {
                this.passkeys[info.profile.id] = '';
            }
            this.base_allowed = _.clone(this.allowed); // reset array to check for changing
            this.base_passkeys = _.clone(this.passkeys); // reset array to check for changing
            this.base_profiles = _.clone(this.profiles); // reset array to check for changing
        },
        passkeyChanged: function () {
            /***
             * callback for change passkey event
             */
            if (info.profile) {
                this.allowed[info.profile.id] = !!this.passkeys[info.profile.id];
            }
        },
        post_allowed_profile_data: function () {
            values = [];
            for (var i in this.profiles) {
                if (this.profiles[i]) {
                    values.push(i);
                }
            }
            return {
                'user': this.id,
                'profiles': values
            }
        },
        reset_profiles: function () {
            this.base_profiles = _.clone(this.profiles);
        },
        sendPasskeyToEmail: function ($event) {
            /***
             * send notification to user about new password
             */
            if (info.profile && !this.sending_email) {
                var that = this;

                // tooltip setup
                var tooltips = $($event.currentTarget).qtip({
                    content: {
                        title: 'status',
                        text: 'email sent'
                    },
                    position: {
                        my: "top center",
                        at: "bottom center"
                    },
                    style: {
                        classes: 'qtip-green qtip-shadow qtip-rounded'
                    },
                    hide: false
                });
                // get  api
                var api = tooltips.qtip('api');
                if (!this.allowed[info.profile.id]) {
                    api.set({
                        'content.text': 'you cant send email for restricted user',
                        'style.classes': 'qtip-red qtip-shadow qtip-rounded'
                    });
                    api.show();
                    setTimeout(function () {
                        api.destroy()
                    }, 2000);
                    return;
                }

                this.sending_email = true;
                $http({
                    method: "POST",
                    url: commonUrls.send_passkey_to_email,
                    data: $.param({
                        "user_id": this.id,
                        "profile_id": info.profile.id,
                        "passkey": this.passkeys[info.profile.id],
                        "csrfmiddlewaretoken": $.cookie("csrftoken")
                    }),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(function () {
                    api.set({
                        'content.text': 'email successfully sent'
                    });

                }).error(function () {
                    api.set({
                        'content.text': 'there was an error, check user email',
                        'style.classes': 'qtip-red qtip-shadow qtip-rounded'
                    });
                })['finally'](function () {
                    that.sending_email = false;
                    // show tooltip and destry in
                    api.show();
                    setTimeout(function () {
                        api.destroy()
                    }, 2000)
                });
            }
        }
    };

    return User;
}]);

