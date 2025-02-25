from rest_framework import viewsets, mixins, filters, pagination
from rest_framework.permissions import IsAuthenticated
from vicharak.models import Role
from vicharak.serializers.roles import RoleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.contrib.auth.models import User


class RolePagination(pagination.LimitOffsetPagination):
    """
    Custom Pagination for Roles

    - Allows offset-based pagination.
    - Default limit: 10
    - Max limit: 100

    """

    default_limit = 10
    max_limit = 100


class RoleViewSet(
    mixins.ListModelMixin,  # GET list
    mixins.RetrieveModelMixin,  # GET detail
    mixins.CreateModelMixin,  # POST
    mixins.UpdateModelMixin,  # PUT/PATCH
    mixins.DestroyModelMixin,  # DELETE
    viewsets.GenericViewSet,
):
    """
    Role ViewSet for managing roles. (List, Create, Retrieve, Update and Delete roles.)

    - Requires authentication.
    - Only staff users can create, update and delete roles.

    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAuthenticated]

    # Add search filter
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]  # Enable searching by role name

    # Add pagination
    pagination_class = RolePagination

    def check_staff_permission(self):
        """Helper function to check if the user is staff."""
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff users can perform this action.")

    def perform_create(self, serializer):
        """Allow only staff users to create a role"""
        self.check_staff_permission()
        serializer.save()

    def perform_update(self, serializer):
        """Allow only staff users to update a role"""
        self.check_staff_permission()
        serializer.save()

    def perform_destroy(self, instance):
        """Allow only staff users to delete a role"""
        self.check_staff_permission()
        instance.delete()

    # ✅ Custom endpoint to assign a role to a user
    # @todo this is just for testing purposes to show how to create custom endpoints in ViewSets with actions
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def assign_role(self, request, pk=None):
        """
        Assigns a role to a user.
        - Only staff can assign roles.
        - Requires 'user_id' in request data.
        """
        self.check_staff_permission()

        role = self.get_object()
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

        # user.role = role  # Assuming `User` model has a `role` field
        # user.save()

        return Response(
            {"message": f"Role '{role.name}' assigned to user '{user.username}'."}
        )
