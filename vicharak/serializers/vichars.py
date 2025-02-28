from rest_framework import serializers
from vicharak.models import Vichar


class VicharSerializer(serializers.ModelSerializer):
    """
    Vichar Serializer for getting vichar details.
    """

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

    # on save, set user to the current user
    def create(self, validated_data):
        user = self.context["request"].user
        print(user, validated_data, "user and validated_data")
        vichar = Vichar.objects.create(user=user, **validated_data)
        return vichar
