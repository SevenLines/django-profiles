# common settings for webassets module
import os
from app.settings import DEBUG, BASE_DIR

ASSETS_MODULES = [
    'app.assets'
]

ASSETS_DEBUG = DEBUG
ASSETS_CACHE = False
ASSETS_MANIFEST = False
if not DEBUG:
    ASSETS_AUTO_BUILD = False

ASSETS_ROOT = os.path.join(BASE_DIR, 'app/static')
