from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, MeView, ChangePasswordView

urlpatterns = [
    # Auth (JWT)
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Users
    path("users/register/", RegisterView.as_view(), name="user-register"),
    path("users/me/", MeView.as_view(), name="user-me"),
    path("users/change-password/", ChangePasswordView.as_view(), name="user-change-password"),
]
