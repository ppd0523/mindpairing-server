from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from mbti.views import *
from .views import *
from board.views import *

# /users/
urlpatterns = [
    # GET
    path('login/kakao/', KakaoLogin.as_view(), name='kakao_login'),
    path('login/kakao/callback/', KakaoLoginCallback.as_view(), name='kakao_callback'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # GET, POST
    path('<nickname>/profile/', UserProfile.as_view(), name='profile'),

    path('imageup', Test1.as_view()),

    # PUT, DELETE
    path('<str:nickname>/posts/<int:post_id>/like', LikePost.as_view(), name='like_post'),
    path('<str:nickname>/posts/<int:post_id>/report', ReportPost.as_view(), name='report_post'),
    path('<str:nickname>/comments/<int:comment_id>/like', LikeComment.as_view(), name='like_comment'),
    path('<str:nickname>/comments/<int:comment_id>/report', ReportComment.as_view(), name='report_comment'),
]