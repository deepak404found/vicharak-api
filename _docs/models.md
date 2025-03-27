# Django Models in Vicharak

## Understanding Django Models 🏗️

Django models define the structure of your database tables and provide an abstraction layer to interact with the database. Each model class maps to a table in the database and includes fields that represent columns.

For more information, refer to the [Django Models documentation](https://docs.djangoproject.com/en/3.2/topics/db/models/).

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

Understanding `related_name`:

- **`related_name`**: Allows you to define the name of the reverse relation from the related object back to this one. This is used to access related objects in reverse, such as `user.vichars.all()`.
- **`related_name` Example**: `user_vichar` in `user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_vichar")`.
- **`related_name` Usage**: `user.vichars.all()` to get all *Vichars* created by a user.
- **`related_name` Default**: If not specified, Django uses the lowercase name of the related model.
- **`related_name` Best Practices**: Use a descriptive name to make the code more readable.
- **`related_name` Caution**: Avoid using `+` or `-` in `related_name` as it may conflict with query syntax.
- **`related_name` Limitation**: It must be unique across the entire Django project.
- **`related_name` Recommendation**: Use plural names for `related_name` to indicate multiple objects.
- **`related_name` Example**: `related_name="user_vichars"` for a one-to-many relationship.

### Understand The relationship between models in Django with the help of the following example

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

## Using Custom Methods 🔧

Custom methods allow us to extend the functionality of models beyond the default behavior provided by Django’s ORM. They make models more versatile and encapsulate reusable logic within the model itself.

### Example: Checking if a User is a Collaborator 👀

```python
class Vichar(models.Model):
    # Fields...
    def is_collaborator(self, user):
        """
        🔎 Checks whether the given user is a collaborator on this Vichar.
        """
        return self.collaborators.filter(collaborator=user).exists()
```

**Usage:**

```python
if vichar.is_collaborator(request.user):
    print("User is a collaborator")
```

### Example: Assigning a Role to a Collaborator 🎭

```python
class Collaborator(models.Model):
    # Fields...
    def assign_role(self, role_name):
        """
        🎭 Assigns a role to the collaborator based on the role name provided.
        """
        role = Role.objects.filter(name=role_name).first()
        if role:
            self.role = role
            self.save()
```

**Usage:**

```python
collaborator.assign_role("EDITOR")
```

---

## Using Models with DRF Serializers 🔄

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

---

## Running Migrations 🚀

After defining models, you need to create database tables using migrations. Run the following commands in the terminal:

1. **Create Migrations:**

    ```bash
    python manage.py makemigrations
    ```

    Or, to create migrations for a specific app:

    ```bash
    python manage.py makemigrations <app_name>
    ```

2. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

This will create the necessary tables in the database based on the models defined in your Django app.

---

## Registering Models in the Admin Panel 🖥

R️egistering models in the Django admin panel allows you to manage data directly from the admin interface. Here’s how you can register the `Vichar` model:

### Admin Panel Registration 📋

Create an `admin.py` file in your app directory and register the model:

```python
from django.contrib import admin
from .models import Vichar

admin.site.register(Vichar)
```

Now, you can access the `Vichar` model from the admin panel and perform CRUD operations easily.

---

## Summary 📝

This guide covers:

- ✅ **Defining models** with fields and relationships
- ✅ **Creating custom methods** for additional functionality
- ✅ **Using models with DRF serializers** for API responses
- ✅ **Querying data** using Django ORM
- ✅ **Running migrations** to update the database
- ✅ **Registering models** in the admin panel

With these concepts, *Vicharak* can efficiently manage thoughts (*Vichars*), collaborators, and roles.

🚀 **Next Step:** Explore Serializers (`serialization.md`) to convert models into API-ready formats.
