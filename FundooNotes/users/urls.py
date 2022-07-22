from django.urls import path
from users.views import (
    RegisterView,
    LogoutAPIView,
    VerifyEmail,
    LoginAPIView,
    SetNewPasswordAPIView,
    ForgotPasswordResetEmailAPIView,
    UserProfileView,
)
from rest_framework_simplejwt.views import (TokenRefreshView, )

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name="register"),
    path('api/login/', LoginAPIView.as_view(), name="login"),
    path('api/logout/', LogoutAPIView.as_view(), name="logout"),
    path('api/email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/forgot-password/', ForgotPasswordResetEmailAPIView.as_view(), name='forgot-password-reset'),
    path('api/reset-password/<uid>/<token>/', SetNewPasswordAPIView.as_view(), name='reset-password'),
    path('api/get-all-users/', UserProfileView.as_view(), name="all_users"),

]
