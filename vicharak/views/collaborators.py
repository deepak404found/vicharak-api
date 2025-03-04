from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from vicharak.models import Collaborator
from vicharak.serializers.collaborators import (
    CollaboratorSerializer,
    AddCollaboratorSerializer,
)


# create a collaborator
class AddCollaboratorView(
    mixins.CreateModelMixin,  # POST
    viewsets.GenericViewSet,
):
    """
    Add Collaborator ViewSet for adding collaborator to a vichar.

    - Requires authentication.
    - user can add collaborators to their vichars.
    """

    queryset = Collaborator.objects.all()
    serializer_class = AddCollaboratorSerializer
    permission_classes = [IsAuthenticated]

    # get collaborators only for the current user
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
