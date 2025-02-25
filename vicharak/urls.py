from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", ListUsersView.as_view(), name="users"),
    path("user/", UserView.as_view(), name="user"),
    path("user/update_password/", UpdatePasswordView.as_view(), name="update_password"),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh token endpoint
]
