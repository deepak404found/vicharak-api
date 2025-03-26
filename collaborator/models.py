from django.db import models
from role.models import Role
from user.models import User
from vichar.models import Vichar


class Collaborator(models.Model):
    """
    Collaborator Model for storing collaborator details

    - Collaborator can have a role
    - Collaborator can be assigned to a vichar by the owner
    - Collaborator can be removed from a vichar by the owner
    - Collaborator can manage the vichar based on the role assigned

    """

    vichar = models.ForeignKey(
        Vichar, on_delete=models.CASCADE, related_name="collaborators"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_vichars"
    )
    collaborator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collaborations"
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, related_name="role"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} / {self.vichar.title} - {self.collaborator.username}"
