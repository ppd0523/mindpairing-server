import os

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView

from config import settings
from .oauth_parameter import *
from .serializers import *

class KakaoLogin(APIView):
    def get(self, request):
        return redirect(f'{KAKAO_OAUTH_URI}&client_id={KAKAO_OAUTH_CLIENT_ID}&redirect_uri={KAKAO_OAUTH_REDIRECT_URI}')


class KakaoLoginCallback(APIView):
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_OAUTH_CLIENT_ID,
            "redirection_uri": KAKAO_OAUTH_REDIRECT_URI,
            "code": request.GET["code"],
        }

        token_info = requests.post(KAKAO_OAUTH_TOKEN_API, data=data).json()

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
    # permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JWTAuthentication, ]

    def get(self, request, nickname):
        serializer = UserProfileSerializer(User.objects.get(nickname=nickname), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, nickname):
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

        try:
            user.image = request.data['image']
            user.update_at = timezone.now()
        except Exception as e:
            pass

        try:
            user.mbti = request.data['mbti']
            user.update_at = timezone.now()
        except Exception as e:
            pass

        user.save()

        return Response({}, status=status.HTTP_200_OK)


class Test1(APIView):
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
