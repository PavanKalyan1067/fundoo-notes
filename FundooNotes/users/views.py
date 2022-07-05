from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.exceptions import (PasswordDidntMatched,
                              PasswordPatternMatchError,
                              UsernameAlreadyExistsError,
                              EmailAlreadyExistsError
                              )

from users.serializers import (RegisterSerializer,
                               LoginSerializer,
                               LogoutSerializer,
                               EmailVerificationSerializer,
                               UserPasswordResetSerializer,
                               PasswordResetSerializer,
                               UserProfileSerializer, ForgotPasswordSerializer
                               )

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
import jwt
from users.renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from users.status import response_code
from users.utils import Util, get_object_by_username, get_object_by_email
from django.conf import settings

from users.validate import validate_password_match, validate_password_pattern_match, \
    validate_duplicat_username_existence, validate_duplicate_email_existence


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        try:
            validate_email(email)
        except ValidationError:
            return Response({'code': 404, 'msg': response_code[404]})
        try:
            validate_password_match(password, confirm_password)
            validate_password_pattern_match(password)
        except PasswordDidntMatched as e:
            return Response({"code": e.code, "msg": e.msg})
        except PasswordPatternMatchError as e:
            return Response({"code": e.code, "msg": e.msg})
        try:
            validate_duplicat_username_existence(username)
        except UsernameAlreadyExistsError as e:
            return Response({"code": e.code, "msg": e.msg})
        try:
            validate_duplicate_email_existence(email)
        except EmailAlreadyExistsError as e:
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
            'message': response_code[200],
            'data': data,
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
                    'success': True,
                    'message': response_code[200],
                }
            return Response(response)
        except jwt.ExpiredSignatureError as e:
            return Response({'code': 304, 'msg': response_code[304]})
        except jwt.exceptions.DecodeError as e:
            return Response({'code': 307, 'msg': response_code[307]})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'code': 410, 'msg': response_code[410]})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(request,email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].authenticated != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].authenticated)

        # if not user:
        #     raise AuthenticationFailed('Invalid credentials, try again')
        if user is not None:
            if user is not user.is_active:
                raise AuthenticationFailed('Account disabled, contact admin')
            if user is user.is_verified:
                raise AuthenticationFailed('Email is not verified')

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetEmailAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'code': 309, 'msg': response_code[309]})


class SetNewPasswordAPIView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'code': 308, 'msg': response_code[308]})


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ({'msg:Logout Successfully!!'})
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class UserProfileView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer
    user = User.objects.all()

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'code': 413, 'msg': response_code[413]})
        user = User.objects.all()
        allUser = RegisterSerializer(user, many=True)
        return Response({'data': allUser.data, 'code': 200, 'msg': response_code[200]})


class ForgotPasswordResetAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        user = get_object_by_email(serializer.data.get('email'))
        # user_email = user.email
        # user = User.objects.get(email=user.email['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to reset your password \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        print(data)
        Util.send_email(data)
        return Response(data, {'msg': response_code[200]})
