from .base import *

ALLOWED_HOSTS = ['*', ]
DEBUG = True

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=100)
DATABASES['default'].update(db_from_env)


# os.environ['KAKAO_OAUTH_CLIENT_ID']
# os.environ['KAKAO_OAUTH_REDIRECT_URI']
