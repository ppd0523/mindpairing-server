from django.urls import path

from board.views import *

urlpatterns = [
    path('', BoardList.as_view(), name='board_list'),
    path('<int:board_index>/topics/<int:topic_index>/', PostList.as_view(), name='board_detail'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='board_detail'),
    # path('messages/', MessageList.as_view(), name='msg_list'),
    # path('messages/<nickname>', MessageDetail.as_view(), name='msg_detail'),
]
