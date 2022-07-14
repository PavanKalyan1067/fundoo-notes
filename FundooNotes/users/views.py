from rest_framework import generics, status
from users.exceptions import (
    PasswordDidntMatched,
    PasswordPatternMatchError
)
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
from users.validate import validate_password_match, validate_password_pattern_match

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        try:
            validate_password_match(password, confirm_password)
            validate_password_pattern_match(password)
        except PasswordDidntMatched as e:
            return Response({"code": e.code, "msg": e.msg})
        except PasswordPatternMatchError as e:
            return Response({"code": e.code, "msg": e.msg})
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
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        Util.send_email(data)
        response = {
            'success': True,
            'msg': response_code[200],
            'data': data
        }
        return Response(response)


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


class ForgotPasswordResetEmailAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status': True,
            'msg': response_code[309]
        }
        return Response(response)


class SetNewPasswordAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'code': 308, 'msg': response_code[308]})


class LogoutAPIView(generics.GenericAPIView):
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


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
