from django.contrib.auth import authenticate
from django.contrib.auth.models import User, update_last_login
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


# Register view
class RegisterView(generics.CreateAPIView):
    """
    Register View for creating a new user with optional fields.

    - Username and password are required.
    - Name and email are optional.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """
    Login View for authenticating a user and generating a token.

    - Username and password are required.
    """

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data, "validated data")
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
            }
        )
