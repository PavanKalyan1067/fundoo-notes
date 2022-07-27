from unittest import TestCase

from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    RegisterView,
    LogoutAPIView,
    VerifyEmail,
    ForgotPasswordResetEmailAPIView,
    SetNewPasswordAPIView,
    UserProfileView,
    LoginAPIView
)


class TestUrls(TestCase):
    def test_registration_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginAPIView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutAPIView)

    def test_EmailVerify_url(self):
        url = reverse('email-verify')
        self.assertEqual(resolve(url).func.view_class, VerifyEmail)

    def test_TokeRefresh_url(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_ForgotPassword_url(self):
        url = reverse('forgot-password-reset')
        self.assertEqual(resolve(url).func.view_class, ForgotPasswordResetEmailAPIView)

    def test_ResetPassword_url(self):
        url = reverse('reset-password', args=['uid', 'token'])
        self.assertEqual(resolve(url).func.view_class, SetNewPasswordAPIView)

    def test_GetAllUsers_url(self):
        url = reverse('all_users')
        self.assertEqual(resolve(url).func.view_class, UserProfileView)
