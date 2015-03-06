# common settings for STATIC, MEDIA and TEMPLATES

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
import os

from app.settings import BASE_DIR

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Note that these paths should use Unix-style forward slashes, even on Windows.
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
