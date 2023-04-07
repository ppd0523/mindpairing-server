import os

KAKAO_OAUTH_URI = "https://kauth.kakao.com/oauth/authorize?response_type=code"
KAKAO_OAUTH_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_OAUTH_REDIRECT_URI = os.environ.get('KAKAO_OAUTH_REDIRECT_URI', None)
KAKAO_OAUTH_CLIENT_ID = os.environ.get("KAKAO_OAUTH_CLIENT_ID", None)
