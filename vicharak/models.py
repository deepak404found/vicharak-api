from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)


class Vichar(models.Model):
    """
    Vichar Model for storing vichar details

    - Vichar is a thought or idea
    - Vichar can be created, updated and deleted by user
    - Vichar can have multiple collaborators

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_vichar")
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    # on delete, set deleted_at to now
    def delete(self, *args, **kwargs):
        # check if permanent delete
        if kwargs.get("permanent"):
            kwargs.pop("permanent")  # remove the permanent delete flag
            super(Vichar, self).delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            self.save()


permissions = [
    "VIEW_VICHAR",
    "EDIT_VICHAR",
    "DELETE_VICHAR",
    "ADD_COLLABORATOR",
    "REMOVE_COLLABORATOR",
    "VIEW_COLLABORATORS",
]


class Role(models.Model):
    """
    Role Model for storing role details

    - Role can have multiple permissions
    - Role can be assigned to collaborators

    """

    name = models.CharField(max_length=50)
    permissions = models.JSONField(
        default=list, help_text="List of permissions for the role."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.permissions = list(set(self.permissions))
        super(Role, self).save(*args, **kwargs)


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
