from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *


class BoardList(APIView):
    @swagger_auto_schema(
        tags=['게시판 기능'],
        operation_description='모든 게시판 정보 반환 API',
        responses={
            200: openapi.Response(
                description='호출 성공',
                schema=openapi.Schema(type=openapi.TYPE_NUMBER)
            )
        }
    )
    def get(self, request):
        """
        모든 카테고리의 게시판과 각 게시판의 토픽 정보 반환

        게시판과 토픽의 index으로 게시글을 얻어올 수 있다
        """
        serializer = BoardSerializer(Board.objects.all(), many=True)
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)


class PostList(APIView):
    @swagger_auto_schema(
        tags=['게시판 기능'],
        operation_summary='',
        responses={
            200: openapi.Response(
                description='호출 성공',
                schema=openapi.Schema(type='Board')
            )
        }
    )
    def get(self, request, board_index=1, topic_index=1):
        """
        게시판 글 목록 보기
        """
        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
            if user_auth_tuple is not None:
                request.user = user_auth_tuple[0]
        except Exception as e:
            request.user = None

        try:
            board = Board.objects.get(index=board_index, hidden=False)
            board_hashtag_assoc = BoardHashtagAssoc.objects.get(board_id=board, index=topic_index, hidden=False)
        except Exception as e:
            return Response({'data': []}, status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(board_id=board, hashtag_id=board_hashtag_assoc.hashtag_id, hidden=False)
        serializer = SimplePostSerializer(posts, user_id=request.user, many=True)

        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)


class PostDetail(APIView):

    def get(self, request, post_id):
        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
            if user_auth_tuple is not None:
                request.user = user_auth_tuple[0]
        except Exception as e:
            request.user = None

        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if post.hidden:
            return Response({'msg': 'This post is hidden'}, status=status.HTTP_204_NO_CONTENT)

        post_serializer = PostDetailSerializer(post, user_id=request.user, many=False)

        comment_serializer = CommentSerializer(post.comment_set.filter(hidden=False), user_id=request.user, many=True)
        return Response({
            'data': {**post_serializer.data},
            'comments': comment_serializer.data,
        }, status=status.HTTP_200_OK)


class MessageList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        q1 = {'sender_id': user, 'delete_at': None}
        q2 = {'receiver_id': user, 'delete_at': None}
        messages = Message.objects.filter(**q1) | Message.objects.filter(**q2)
        conversation = {}
        for message in messages:
            m = {
                'last_content': message.content,
                'create_at': message.create_at,
            }
            if message.sender_id == user:
                m['that_nickname'] = message.receiver_id.nickname
                conversation[message.receiver_id.nickname] = m
            else:
                m['that_nickname'] = message.sender_id.nickname
                conversation[message.sender_id.nickname] = m

        message_list = [m for m in conversation.values()]

        return Response(message_list, status=status.HTTP_200_OK)


class MessageDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, nickname):
        """
        Return messages with me and <nickname>
        """
        user = request.user
        _nickname = User.objects.get(nickname=nickname)
        q1 = {'sender_id': user, 'receiver_id': _nickname, 'delete_at': None}
        q2 = {'sender_id': _nickname, 'receiver_id': user, 'delete_at': None}
        messages = Message.objects.filter(**q1) | Message.objects.filter(**q2)
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePost(APIView):
    def put(self, request, nickname=None, post_id=None):
        return Response({})

    def delete(self, request, nickname=None, post_id=None):
        return Response({})


class ReportPost(APIView):
    def put(self, request, nickname=None, post_id=None):
        return Response({})

    def delete(self, request, nickname=None, post_id=None):
        return Response({})


class LikeComment(APIView):
    def put(self, request, nickname=None, comment_id=None):
        return Response({})

    def delete(self, request, nickname=None, comment_id=None):
        return Response({})


class ReportComment(APIView):
    def put(self, request, nickname=None, comment_id=None):
        return Response({})

    def delete(self, request, nickname=None, comment_id=None):
        return Response({})
