from rest_framework import serializers
from collaborator.models import Collaborator
from role.models import Role


class CollaboratorSerializer(serializers.ModelSerializer):
    """
    Collaborator Serializer for getting collaborator details.
    """

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Collaborator
        fields = "__all__"
        read_only_fields = ("id",)

    def get_permissions(self, obj):
        role = Role.objects.filter(id=obj.role.id)
        permissions = role[0].permissions
        return permissions

    def __str__(self):
        return f"{self.owner.username} / {self.vichar.title} - {self.collaborator.username}"
