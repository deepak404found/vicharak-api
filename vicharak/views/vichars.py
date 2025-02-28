from rest_framework import viewsets, mixins, filters, pagination
from rest_framework.permissions import IsAuthenticated
from vicharak.models import Vichar
from vicharak.serializers.vichars import VicharSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from vicharak.models import User


class VicharViewSet(
    mixins.ListModelMixin,  # GET list
    mixins.RetrieveModelMixin,  # GET detail
    mixins.CreateModelMixin,  # POST
    mixins.UpdateModelMixin,  # PUT/PATCH
    mixins.DestroyModelMixin,  # DELETE
    viewsets.GenericViewSet,
):
    """
    Vichar ViewSet for managing vichars. (List, Create, Retrieve, Update and Delete vichars.)

    - Requires authentication.
    - user can access only their vichars.
    - users can create, update and delete vichars.

    """

    queryset = Vichar.objects.all()
    serializer_class = VicharSerializer
    permission_classes = [IsAuthenticated]

    # Add search filter
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]  # Enable searching by title

    # get vichars only for the current user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
