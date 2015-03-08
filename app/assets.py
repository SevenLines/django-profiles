from django_assets import Bundle, register

base_js = Bundle('vendor/jquery/dist/jquery.min.js',
                 'vendor/jquery-cookie/jquery.cookie.js',
                 'vendor/lodash/lodash.min.js',
                 'lib/qtip/jquery.qtip.js',
                 'js/main.js',
                 filters="jsmin",
                 output="js/dist/base.js")

profiles_manager_js = Bundle('vendor/angular/angular.js',
                            'js/manager/app.js',
                            'js/manager/models/user.js',
                            'js/manager/controllers/profiles.js',
                            'js/manager/controllers/users.js',
                            filters="jsmin",
                            output="js/dist/profiles-manager.js")

base_css = Bundle('vendor/bootstrap/dist/css/bootstrap.css',
                  'lib/qtip/jquery.qtip.css',
                  'css/style.css',
                  filters="cssmin",
                  output="js/dist/base.css")

# javascript
register("base-js", base_js)
register("profiles-manager-js", profiles_manager_js)

# styles
register("base-css", base_css)