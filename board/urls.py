from django.urls import path

from board.views import *

# /boards/...
urlpatterns = [
    path('', BoardList.as_view(), name='board_list'),
    # path('<str:category>/topics/<str:topic>/posts/', PostListByName.as_view(), name='post_list_by_name'),
    path('<int:board_index>/topics/<int:topic_index>/posts/', PostListByIndex.as_view(), name='post_list_by_index'),
    # get, post, delete
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    # put
    path('posts/', CreatePost.as_view(), name='create_post_detail'),

    # put, delete
    path('posts/<int:post_id>/like/', LikePost.as_view(), name='like_post')
    # path('messages/', MessageList.as_view(), name='msg_list'),
    # path('messages/<nickname>', MessageDetail.as_view(), name='msg_detail'),
]
