from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from users.serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    UserPasswordResetSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
import jwt
from users.renderers import UserRenderer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from users.status import response_code
from users.utils import Util
from django.conf import settings

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

'''
RegisterView(generics.GenericAPIView) is for registering a new user
'''


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'from_email': settings.EMAIL_HOST_USER,
                'email_subject': 'Verify your email'}
        Util.send_email(data)
        response = {
            'success': True,
            'msg': response_code[200],
            'data': user_data
        }
        return Response(response)


'''
VerifyEmail(generics.GenericAPIView) is for Verifying email for new user after registration
'''


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            print('payload 1 ' + str(payload))
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                response = {
                    'status': True,
                    'msg': response_code[302]
                }
                return Response(response)
        except jwt.ExpiredSignatureError as e:
            response = {
                'status': True,
                'msg': response_code[304]
            }
            return Response(response)
        except jwt.exceptions.DecodeError as e:
            response = {
                'status': True,
                'msg': response_code[307]
            }
            return Response(response)


'''ForgotPasswordResetEmailAPIView(generics.GenericAPIView) is for it will send the link to email to reset the 
password for existing user
'''


class ForgotPasswordResetEmailAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status': True,
            'msg': response_code[309]
        }
        return Response(response)


'''
SetNewPasswordAPIView(generics.GenericAPIView) is for updating new password for Existing user
'''


class SetNewPasswordAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserPasswordResetSerializer

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        response = {
            'status': True,
            'msg': response_code[308]
        }
        return Response(response)


'''
LogoutAPIView(generics.GenericAPIView) is for logging out the user
'''


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            Refresh_token = request.data["refresh"]
            token = RefreshToken(Refresh_token)
            token.blacklist()
            response = ({
                'success': True,
                'msg': response_code[417]
            })
            return Response(response)
        except Exception as e:
            response = ({
                'success': True,
                'msg': response_code[418]
            })
            return Response(response)


'''
UserProfileView(generics.GenericAPIView) is for get all the users who have registered
'''


class UserProfileView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def get(self, request):
        try:
            user = User.objects.all()
            allUser = RegisterSerializer(user, many=True)
            response = ({
                'Success': True,
                'msg': response_code[200],
                'data': allUser.data})
            return Response(response)
        except Exception as e:
            response = ({
                'success': False,
                'msg': response_code[416]
            })
            return Response(response)


'''
LoginAPIView(generics.GenericAPIView) is for Login for user who have registered
'''


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response = {
            'status': True,
            'msg': response_code[419],
            'data': serializer.data
        }
        return Response(response)
