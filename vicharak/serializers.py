from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer for getting user details, excluding sensitive information.

    - Ensures email is unique.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        exclude = ("password",)  # Exclude password for security

    def validate_email(self, value):
        """Ensure email is unique, excluding the current user (for updates)."""
        print(self.instance, "email")
        if (
            self.instance
            and User.objects.exclude(id=getattr(self.instance, "id", None))
            .filter(email=value)
            .exists()
        ):
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        """Ensure username is unique, excluding the current user (for updates)."""
        print(self.instance, "username")
        if (
            self.instance
            and User.objects.exclude(id=getattr(self.instance, "id", None))
            .filter(username=value)
            .exists()
        ):
            raise serializers.ValidationError("Username is already in use.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register Serializer for creating a new user with optional fields.

    - Username and password are required.
    - Name and email are optional.
    """

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        min_length=8,
        max_length=64,
    )
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ("id", "name", "email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create a new user with hashed password"""
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  # ✅ Securely set the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user, username, password, "user")
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg)
        else:
            msg = "Must include 'username' and 'password'."
            raise serializers.ValidationError(msg)

        data["user"] = user
        return data
