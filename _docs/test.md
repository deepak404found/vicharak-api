# Django Models in Vicharak

## Understanding Django Models 🏗️
Django models define the structure of your database tables and provide an abstraction layer to interact with the database. Each model class maps to a table in the database and includes fields that represent columns.

In *Vicharak*, models are used to manage thoughts (*Vichars*), user roles, and collaborators.

---

## Defining Models ✍️
A model in Django is a class that subclasses `models.Model`. Here’s the `Vichar` model from *Vicharak*:

### Vichar Model 🧠
```python
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Vichar(models.Model):
    """
    📌 Vichar Model for storing vichar details

    - 📝 Vichar is a thought or idea
    - 🔄 Vichar can be created, updated and deleted by users
    - 🤝 Vichar can have multiple collaborators
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_vichar")
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    # Custom delete method
    def delete(self, *args, **kwargs):
        """
        🗑️ Soft delete by setting deleted_at timestamp instead of permanently deleting the record.
        """
        if kwargs.get("permanent"):
            kwargs.pop("permanent")
            super(Vichar, self).delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            self.save()
```

### Explanation 📖
- **Fields**: `CharField`, `TextField`, and `DateTimeField` store title, body, and timestamps.
- **Relationships**: `ForeignKey(User)` establishes a one-to-many relationship.
- **Custom Delete Method**: Supports soft deletion by setting `deleted_at` instead of permanently removing the record.

---

## Model Relationships 🔗
Django provides several relationship types:
- **🔄 One-to-One (`OneToOneField`)**: Used when one record is strictly linked to another, such as a user profile.
- **🔀 One-to-Many (`ForeignKey`)**: A single record can be linked to multiple related records, such as a user having multiple thoughts (*Vichars*).
- **🔗 Many-to-Many (`ManyToManyField`)**: Both sides of the relationship can have multiple related objects, such as users and groups.

### Collaborator Model 🤝
```python
from role.models import Role
from user.models import User
from vichar.models import Vichar

class Collaborator(models.Model):
    """
    🤝 Collaborator Model for storing collaborator details
    
    - A collaborator is a user who is given access to a specific *Vichar*.
    - 👤 Collaborators can be assigned roles with specific permissions.
    - 👑 The owner of the *Vichar* can manage collaborators.
    """
    vichar = models.ForeignKey(Vichar, on_delete=models.CASCADE, related_name="collaborators")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_vichars")
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborations")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name="role")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} / {self.vichar.title} - {self.collaborator.username}"
```

#### Explanation 📌
- **🔗 `ForeignKey(Vichar)`**: Many collaborators can be linked to a single *Vichar*.
- **🔄 `ForeignKey(Role)`**: Each collaborator has an assigned role.
- **🔍 `related_name`**: Provides reverse query capabilities (e.g., `vichar.collaborators.all()`).

---

## Using Models with DRF Serializers 🔄
Django Rest Framework (DRF) provides serializers to convert complex data types like models into JSON. Serializers help in querying and managing data efficiently.

### Querying Data with Models 🔍
Using Django ORM, you can query model data like this:
```python
# Get all vichars
vichars = Vichar.objects.all()

# Get a specific vichar by ID
vichar = Vichar.objects.get(id=1)

# Filter vichars by user
user_vichars = Vichar.objects.filter(user=request.user)
```
### Managing Data with Serializers 📤
To expose model data through an API, create a serializer:
```python
from rest_framework import serializers
from .models import Vichar

class VicharSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vichar
        fields = '__all__'
```
This serializer can now be used in views to return JSON responses.

---

## Model Permissions 🔒
Permissions define what actions a user can perform. *Vicharak* has:
```python
permissions = [
    "👀 VIEW_VICHAR",
    "✏️ EDIT_VICHAR",
    "🗑️ DELETE_VICHAR",
    "➕ ADD_COLLABORATOR",
    "❌ REMOVE_COLLABORATOR",
    "👥 VIEW_COLLABORATORS",
]
```
These permissions can be stored in the `Role` model:

### Role Model 🎭
```python
class Role(models.Model):
    """
    🎭 Role Model to manage different levels of access permissions for collaborators.
    """
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=list, help_text="List of permissions for the role.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        ✅ Ensure that permissions remain unique before saving the role.
        """
        self.permissions = list(set(self.permissions))
        super(Role, self).save(*args, **kwargs)
```

---

## Conclusion 🎯
This guide covers:
✅ **Defining models** with fields and relationships
✅ **Using DRF serializers** for querying and managing data
✅ **Creating custom methods** for additional functionality
✅ **Implementing permissions and roles** for access control
✅ **Running migrations** to update the database
✅ **Registering models** in the admin panel

With these concepts, *Vicharak* can efficiently manage thoughts (*Vichars*), collaborators, and roles.

🚀 **Next Step:** Explore Serializers (`serialization.md`) to convert models into API-ready formats.

