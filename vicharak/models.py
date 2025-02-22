from django.db import models
from django.contrib.auth.models import User

# (
#     BaseUserManager,
#     AbstractBaseUser,
#     PermissionsMixin,
# )


# class UserManager(BaseUserManager):
#     """
#     Custom User Manager for creating users with email as the unique identifier
#     """

#     def create_user(self, username, email=None, password=None, **extra_fields):
#         """
#         Create and return a regular user with an email, username, and password
#         """
#         if not username:
#             raise ValueError("The Username field must be set")

#         email = self.normalize_email(email) if email else None
#         extra_fields.setdefault("is_active", True)

#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         """
#         Create and return a superuser with username, email, and password
#         """
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(
#             username=username, email=email, password=password, **extra_fields
#         )


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Custom User Model for authentication and Vicharak management
#     """

#     name = models.CharField(max_length=50, blank=True, null=True)
#     email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=128)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     last_login = models.DateTimeField(null=True, blank=True)

#     is_active = models.BooleanField(default=True)  # Required by Django auth
#     is_staff = models.BooleanField(default=True)  # Admin site access

#     # Avoid conflicts with Django's built-in User model
#     groups = models.ManyToManyField(
#         "auth.Group", related_name="vicharak_users", blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission", related_name="vicharak_users_permissions", blank=True
#     )

#     objects = UserManager()

#     USERNAME_FIELD = "username"  # Used for authentication
#     REQUIRED_FIELDS = ["email"]  # Email is required for superusers

#     def __str__(self):
#         return self.username


class Vichar(models.Model):
    """
    Vichar Model for storing vichar details

    - Vichar is a thought or idea
    - Vichar can be created, updated and deleted by user
    - Vichar can have multiple collaborators

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


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
    permissions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    """
    Collaborator Model for storing collaborator details

    - Collaborator can have a role
    - Collaborator can be assigned to a vichar by the owner
    - Collaborator can be removed from a vichar by the owner
    - Collaborator can manage the vichar based on the role assigned

    """

    vichar = models.ForeignKey(Vichar, on_delete=models.CASCADE, related_name="vichar")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    collaborator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collaborator"
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vichar.title + " - " + self.user.name
