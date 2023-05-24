from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView

from config import settings
from .oauth_parameter import *
from .serializers import *


class KakaoLoginAuth(APIView):
    @swagger_auto_schema(
        tags=['로그인'],
        operation_id='kakao_login_auth_post',
        operation_summary='카카오 로그인',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Kakao access token. Key is authorize-access-token in Cookie',
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description='서비스 이용 토큰 반환과 유저 정보 반환',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_init': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'mbti': openapi.Schema(type=openapi.TYPE_STRING),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'create_at': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description='Invalid access_token',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )
            ),
        }
    )
    def post(self, request):
        """
        Get access token
        """

        if 'access_token' not in request.data:
            return Response({'msg': 'request body NOT include \'access_token\''}, status=status.HTTP_400_BAD_REQUEST)

        me_url = "https://kapi.kakao.com/v2/user/me"
        res = requests.get(me_url, headers={
            "Authorization": f"Bearer {request.data['access_token']}"})

        if res.status_code != 200:
            return Response({'msg': 'request body should be in \'access_token\''}, status=status.HTTP_400_BAD_REQUEST)

        kakao_resource = res.json()  # {'id': <int>, 'connected_at': '2023-05-01T08:21:33Z', 'properties': {'nickname': '이강현'}, 'kakao_account': {'profile_nickname_needs_agreement': False, 'profile': {'nickname': '이강현'}}}

        kakao_id = kakao_resource['id']

        oa, oa_created = OpenAuth.objects.get_or_create(kakao=f'k{kakao_id}')

        if oa_created:
            user = User.objects.create_user(nickname=f'k{kakao_id}')

            oa.user_id = user
            oa.kakao_update_at = timezone.now()
            user.save()
            oa.save()
        else:
            user = oa.user_id

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return Response({
            "nickname": user.nickname,
            "mbti": user.mbti,
            "is_init": user.is_init,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, status=status.HTTP_200_OK)


class KakaoLoginWeb(APIView):

    @swagger_auto_schema(
        operation_summary='For Server test only'
    )
    def get(self, request):
        uri = f"{KAKAO_OAUTH_URI}&client_id={KAKAO_OAUTH_CLIENT_ID}&redirect_uri={KAKAO_OAUTH_REDIRECT_URI}"
        return redirect(uri)


class KakaoLoginWebCallback(APIView):
    @swagger_auto_schema(
        operation_summary='For Server test only'
    )
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_OAUTH_CLIENT_ID,
            "redirection_uri": KAKAO_OAUTH_REDIRECT_URI,
            "code": request.GET["code"],
        }

        # token_info = requests.post(KAKAO_OAUTH_TOKEN_API, data=data, headers={"Content-Type" : "application/json"}).json()
        token_info = requests.post(KAKAO_OAUTH_TOKEN_API, data=data, headers={"Content-Type" : "application/x-www-form-urlencoded"}).json()

        access_token = token_info["access_token"]
        kakao_resource = requests.get("https://kapi.kakao.com/v2/user/me", headers={
            "Authorization": f"Bearer {access_token}"}).json()

        oa, oa_created = OpenAuth.objects.get_or_create(kakao=kakao_resource['id'])

        if oa_created:
            user = User.objects.create_user(nickname=f"k{kakao_resource['id']}")

            oa.user_id = user
            oa.kakao_update_at = timezone.now()
            user.save()
            oa.save()
        else:
            user = oa.user_id

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        return Response({
            "nickname": user.nickname,
            "mbti": user.mbti,
            "is_init": user.is_init,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, status=status.HTTP_200_OK)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    @swagger_auto_schema(
        tags=['회원 정보'],
        operation_id='user_profile_get',
        operation_summary='내 정보 얻기',
        manual_parameters=[
        ],
        responses={
            200: openapi.Response(
                description='유저 정보',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                        'image': openapi.Schema(type=openapi.TYPE_STRING),
                        'mbti': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'create_at': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description='Invalid access_token',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )
            ),
        }
    )
    def get(self, request):
        serializer = UserProfileSerializer(User.objects.get(nickname=request.user.nickname), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['회원 정보'],
        operation_id='user_profile_post',
        operation_summary='내 정보 수정',
        request_body=openapi.Schema(
            description="변경 할 데이터를 body 에 포함하여 전송할 경우 해당 필드의 정보만 수정 됨",
            type=openapi.TYPE_OBJECT,
            properties={
                'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                'mbti': openapi.Schema(type=openapi.TYPE_STRING, description='소문자 [iesntfpj]만 허용'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='한글자 [남여]만 허용'),
            },
        ),
        responses={
            200: openapi.Response(
                description='서비스 이용 토큰 반환과 유저 정보 반환',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description='Invalid access_token',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                )
            ),
        }
    )
    def post(self, request):
        user = request.user

        try:
            # if timezone.now() - user.update_at > django.utils.timezone.timedelta(=120):
            # if timezone.now().day == 16:
            user.nickname = request.data['nickname']
            user.update_at = timezone.now()
            user.is_init = True

        except Exception as e:
            pass

        try:
            user.phone = request.data['phone']
            user.update_at = timezone.now()
        except Exception as e:
            pass

        try:
            user.email = request.data['email']
            user.update_at = timezone.now()
        except Exception as e:
            pass

        # try:
        #     user.image = request.data['image']
        #     user.update_at = timezone.now()
        # except Exception as e:
        #     pass

        try:
            user.mbti = request.data['mbti']
            user.update_at = timezone.now()
        except Exception as e:
            pass

        user.save()

        return Response({}, status=status.HTTP_200_OK)


class ImageView(APIView):
    def post(self, request):
        user = User.objects.get(nickname='ppd0523')

        image = request.data['image']
        filename = os.path.basename(image.name)
        # blob = bucket.blob(filename)
        # blob.upload_from_file(image, content_type='image/png')
        # public_url = blob.public_url

        return Response({'msg': 'asdf'}, status=status.HTTP_200_OK)

    # def get(self, request):
    #     blob = bucket.blob('east.png')
    #     if blob:
    #         data = blob.download_as_bytes()
    #         response = HttpResponse(
    #             data,
    #             content_type=blob.content_type,
    #             status=status.HTTP_200_OK,
    #         )
    #         response['Content-Disposition'] = f'attachment; filename="east.png"'
    #         return response
    #
    #     return Response({'data': 'ok'}, status=status.HTTP_200_OK)


def kakaoLoginTestPage(request, ):
    return render(request, 'membership/login.html', )
