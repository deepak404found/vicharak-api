from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import users, roles, vichars
from rest_framework_simplejwt.views import TokenRefreshView

# Router for ViewSets
router = DefaultRouter()
router.register(r"vichars", vichars.VicharViewSet, basename="vichars")
# router.register(r'collaborators', CollaboratorViewSet, basename='collaborators')
router.register(r"roles", roles.RoleViewSet, basename="roles")

urlpatterns = [
    path("register/", users.RegisterView.as_view(), name="register"),
    path("login/", users.LoginView.as_view(), name="login"),
    path("users/", users.ListUsersView.as_view(), name="users"),
    path("user/", users.UserView.as_view(), name="user"),
    path(
        "user/update_password/",
        users.UpdatePasswordView.as_view(),
        name="update_password",
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh token endpoint
    path("", include(router.urls)),  # Include router URLs
]
