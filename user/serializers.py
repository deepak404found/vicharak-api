from rest_framework import serializers
from user.models import User
from rest_framework.validators import UniqueValidator


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
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "date_joined", "last_login")
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate_email(self, value):
        """Ensure email is unique, excluding the current user (for updates)."""
        if (
            self.instance
            and User.objects.exclude(id=getattr(self.instance, "id", None))
            .filter(email=value)
            .exists()
        ):
            raise serializers.ValidationError("Email is already in use.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register Serializer for creating a new user with optional fields.

    - Username and password are required.
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
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "first_name", "last_name")
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
        min_length=8,
        max_length=64,
    )


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        min_length=8,
        max_length=64,
    )
    new_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        min_length=8,
        max_length=64,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        min_length=8,
        max_length=64,
    )
