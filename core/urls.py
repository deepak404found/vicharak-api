"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from role.views import RoleViewSet
from vichar.views import VicharViewSet
from user.views import (
    ListUsersView,
    LoginView,
    RegisterView,
    UpdatePasswordView,
    UserView,
)

# Router for ViewSets
router = DefaultRouter()
router.register(r"vichars", VicharViewSet, basename="vichars")
router.register(r"roles", RoleViewSet, basename="roles")

# URLs for Vicharak API
vicharak_urls = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", ListUsersView.as_view(), name="users"),
    path("user/", UserView.as_view(), name="user"),
    path(
        "user/update_password/",
        UpdatePasswordView.as_view(),
        name="update_password",
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh token endpoint
    path("", include(router.urls)),  # Include router URLs
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "vicharak-api/", include(vicharak_urls)
    ),  # Include Vicharak URLs with prefix vicharak-api
]
