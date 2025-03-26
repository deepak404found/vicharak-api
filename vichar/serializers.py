from django.utils import timezone
from django.db.models import Q
from django.http import Http404
from rest_framework import serializers

from collaborator.models import Collaborator
from collaborator.serializers import CollaboratorSerializer
from role.models import Role
from user.models import User
from vichar.models import Vichar


class VicharSerializer(serializers.ModelSerializer):
    """
    Vichar Serializer for getting vichar details.
    """

    collaborators = serializers.SerializerMethodField()

    class Meta:
        model = Vichar
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            "title": {"required": True},
            "body": {"required": True},
            "user": {"required": False},
        }

    def __str__(self):
        return self.title

    def get_collaborators(self, obj):
        collaborators = Collaborator.objects.filter(vichar=obj)
        collaborators = CollaboratorSerializer(collaborators, many=True).data

        is_owner = obj.user == self.context["request"].user
        has_permission = self.validate_collaborator(
            obj.id, self.context["request"].user.id, "VIEW_COLLABORATORS"
        )

        if is_owner or has_permission:
            return collaborators
        return []

    # on save, set user to the current user
    def create(self, validated_data):
        user = self.context["request"].user
        vichar = Vichar.objects.create(user=user, **validated_data)
        return vichar

    def update(self, instance, validated_data):
        is_owner = instance.user == self.context["request"].user
        has_permission = self.validate_collaborator(
            instance.id, self.context["request"].user.id, "EDIT_VICHAR"
        )

        # check if user is owner or has permission to edit the vichar
        if is_owner or has_permission:
            # update date with now
            instance.updated_at = timezone.now()
            return super().update(instance, validated_data)

        raise serializers.ValidationError(
            {
                "detail": "You do not have permission to edit this vichar.",
            }
        )

    def delete(self, instance):
        is_owner = instance.user == self.context["request"].user
        has_permission = self.validate_collaborator(
            instance.id, self.context["request"].user.id, "DELETE_VICHAR"
        )

        # check if user is owner or has permission to delete the vichar
        if is_owner or has_permission:
            instance.delete()
            return instance

        raise serializers.ValidationError(
            {
                "detail": "You do not have permission to delete this vichar.",
            }
        )

    def validate_collaborator(self, vicharId, collaborator, permission):
        """
        Validate if the collaborator has the required permission.

        Args:
            vicharId (int): Vichar ID.
            collaborator (int): Collaborator ID.
            permission (str): Permission to check.

        Returns:
            bool: True if collaborator has the required permission, False otherwise.
        """
        collaborator = Collaborator.objects.filter(
            vichar=vicharId, collaborator=collaborator
        ).first()
        if not collaborator:
            return False

        collaborator = CollaboratorSerializer(collaborator).data
        if permission in collaborator["permissions"]:
            return True
        return False


class AddCollaboratorSerializer(serializers.ModelSerializer):
    """
    Add Collaborator Serializer for adding collaborator to a vichar.
    """

    vichar = serializers.PrimaryKeyRelatedField(
        queryset=Vichar.objects.all(),
        required=False,
        write_only=True,
        help_text="Vichar ID",
    )
    collaborator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        help_text="Collaborator ID",
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=True,
        write_only=True,
        help_text="Role ID",
    )

    class Meta:
        model = Collaborator
        fields = ["vichar", "collaborator", "role"]
        read_only_fields = ("id", "owner")

    # set owner to the current user
    def create(self, validated_data):
        # owner cannot be a collaborator
        if validated_data["vichar"].user == validated_data["collaborator"]:
            raise serializers.ValidationError("Owner cannot be a collaborator.")

        is_owner = validated_data["vichar"].user == self.context["request"].user
        v_serializer = VicharSerializer(validated_data["vichar"], context=self.context)
        has_permission = v_serializer.validate_collaborator(
            validated_data["vichar"].id,
            self.context["request"].user.id,
            "ADD_COLLABORATOR",
        )

        # raise an error if user is not owner and does not have permission
        if not is_owner and not has_permission:
            raise serializers.ValidationError(
                "You do not have permission to add collaborator."
            )

        # check if collaborator already exists; if yes, raise an error
        collaborator = Collaborator.objects.filter(
            vichar=validated_data["vichar"], collaborator=validated_data["collaborator"]
        ).first()
        if collaborator:
            raise serializers.ValidationError("Collaborator already exists.")

        # create collaborator with owner as the user of vichar
        validated_data["owner"] = validated_data["vichar"].user
        collaborator = Collaborator.objects.create(**validated_data)
        return collaborator

    # get collaborator and update the role
    def update(self, validated_data):
        """
        Update the collaborator's role.

        Args:
            validated_data (dict): Validated data from the serializer.

        Returns:
            Collaborator: Updated collaborator instance.

        Raises:
            Http404: If collaborator does not exist.
        """

        # try to get the collaborator first
        try:
            collaborator = Collaborator.objects.get(
                vichar=validated_data["vichar"],
                collaborator=validated_data["collaborator"],
            )
        except Collaborator.DoesNotExist:
            raise Http404("Collaborator does not exist.")

        # update the collaborator
        collaborator.role = validated_data["role"]
        collaborator.save()
        return collaborator


class RemoveCollaboratorSerializer(serializers.ModelSerializer):
    collaborator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        help_text="Collaborator ID",
    )

    class Meta:
        model = Collaborator
        fields = ["vichar", "collaborator"]
        read_only_fields = ("id", "owner")

    def delete(self, validated_data):
        """
        Delete the collaborator.
        """

        # try to get the collaborator first
        try:
            collaborator = Collaborator.objects.get(
                vichar=validated_data["vichar"],
                collaborator=validated_data["collaborator"],
            )
        except Collaborator.DoesNotExist:
            raise Http404("Collaborator does not exist.")

        collaborator.delete()
        return collaborator
