from rest_framework import serializers
from vicharak.models import Role
from rest_framework.validators import UniqueValidator


class RoleSerializer(serializers.ModelSerializer):
    """
    Role Serializer for getting role details.
    - Ensures name is unique.
    """

    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Role.objects.all())],
    )
    permissions = serializers.JSONField(
        required=True,
        help_text="List of permissions for the role.",
    )

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {"name": {"required": True}, "permissions": {"required": True}}

    def __str__(self):
        return self.name
