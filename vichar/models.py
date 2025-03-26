from django.db import models
from django.utils import timezone
from user.models import User


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
