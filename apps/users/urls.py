from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    UserListApiView,
    RefreshTokenView,
    SendCodeView,
    VerifyCodeView,
    SendOTPView,
    VerifyOTPView,
)

urlpatterns = [
    # OTP Flow (2025–2026)
    path("auth/send-otp/", SendOTPView.as_view(), name="auth-send-otp"),
    path("auth/verify-otp/", VerifyOTPView.as_view(), name="auth-verify-otp"),
    # Auth (tz.json / legacy)
    path("auth/send-code/", SendCodeView.as_view(), name="auth-send-code"),
    path("auth/verify/", VerifyCodeView.as_view(), name="auth-verify"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    # Legacy / aliases
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListApiView.as_view(), name="user-list"),
]