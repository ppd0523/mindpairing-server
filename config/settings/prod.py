from .base import *

ALLOWED_HOSTS = ['*', ]
DEBUG = True

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=100)
DATABASES['default'].update(db_from_env)

FIREBASE_INFO.update({
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID', None),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY', None),
})
