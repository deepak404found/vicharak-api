from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from vicharak.models import Vichar
from vicharak.serializers.collaborators import CollaboratorSerializer
from vicharak.serializers.vichars import AddCollaboratorSerializer, VicharSerializer
from django.db.models import Q


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

    # get current user's vichars and vichars where the current user is a collaborator
    def get_queryset(self):
        return Vichar.objects.filter(
            Q(user=self.request.user) | Q(collaborators__collaborator=self.request.user)
        ).distinct()

    # update the vichar with PUT method; PATH is not working properly
    def partial_update(self, request, *args, **kwargs):
        vichar = self.get_object()
        serializer = self.get_serializer(vichar, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        super().partial_update(request, *args, **kwargs)
        return Response(serializer.data)

    # action to add collaborators to a vichar
    @action(detail=True, methods=["post"])
    def add_collaborator(self, request, pk=None):
        vichar = self.get_object()
        serializer = AddCollaboratorSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # add collaborator
            collaborator = serializer.save(vichar=vichar)
            return Response(
                {
                    "message": "Collaborator added successfully.",
                    "data": CollaboratorSerializer(collaborator).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # action to update collaborators of a vichar
    @action(detail=True, methods=["put"])
    def update_collaborator(self, request, pk=None):
        vichar = self.get_object()
        request.data["vichar"] = vichar.id
        serializer = AddCollaboratorSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            # update collaborator
            collaborator = serializer.update(serializer.validated_data)
            return Response(
                {
                    "message": "Collaborator updated successfully.",
                    "data": CollaboratorSerializer(collaborator).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
