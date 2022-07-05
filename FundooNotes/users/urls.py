from django.urls import path
from users.views import (
    RegisterView,
    LogoutAPIView,
    VerifyEmail,
    LoginAPIView,
    SetNewPasswordAPIView,
    PasswordResetEmailAPIView,
    UserProfileView,
ForgotPasswordResetAPIView,
)
from rest_framework_simplejwt.views import (TokenRefreshView, )

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('forgot-password/', ForgotPasswordResetAPIView.as_view(), name='forgot-password-reset'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-complete/', PasswordResetEmailAPIView.as_view(),
         name='password-reset-complete'),
    path('reset-password/<uid>/<token>/', SetNewPasswordAPIView.as_view(), name='reset-password'),
    path('get-all-users/', UserProfileView.as_view(), name="all_users"),

]
