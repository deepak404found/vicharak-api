from django.contrib.auth import authenticate
from django.contrib.auth.models import User, update_last_login
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from vicharak.serializers.users import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    UpdatePasswordSerializer,
)


# Register view
class RegisterView(generics.CreateAPIView):
    """
    Register View for creating a new user with optional fields.

    - Username and password are required.
    - Name and email are optional.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# login view
class LoginView(APIView):
    """
    Login View for authenticating a user and generating a token.

    - Username and password are required.
    """

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        update_last_login(None, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


# list all users view
class ListUsersView(generics.ListAPIView):
    """
    List Users View for getting a list of all users.

    - Requires authentication.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# user view for CRUD operations on current user
class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    User View for getting and updating the current user.

    - Requires authentication.

    - GET: Get user details.
    - PATCH: Update user details.
    - DELETE: Delete user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Get logged-in user

    # disable put method
    def put(self, request, *args, **kwargs):
        return Response(
            {"error": "This method is not allowed, use PATCH instead for updates."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# update password view for updating the current user's password
class UpdatePasswordView(APIView):
    """
    Reset Password View for updating the current user's password
    with a new one by providing the current password.

    - Requires authentication.
    - Current password is required.
    - New password is required.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def post(self, request):
        user = self.request.user
        # validate serializer
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get data from serializer
        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        # match new password and confirm password
        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if current password is correct
        if not user.check_password(current_password):
            return Response(
                {"error": "Invalid current password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # update password
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully."})
