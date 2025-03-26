from django.db import models

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
