from django_assets import Bundle, register

base_js = Bundle('vendor/jquery/dist/jquery.min.js',
                 'vendor/jquery-cookie/jquery.cookie.js',
                 'vendor/lodash/lodash.min.js',
                 'js/main.js',
                 filters="jsmin",
                 output="js/dist/base.js")

base_css = Bundle('vendor/bootstrap/dist/css/bootstrap.css',
                  'css/style.css',
                  filters="cssmin",
                  output="js/dist/base.css")

register("base-js", base_js)
register("base-css", base_css)