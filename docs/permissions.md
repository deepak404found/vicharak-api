# Django Permissions Tutorial

Permissions in Django determine whether a user or group has the necessary rights to perform specific actions. Django's permission system works with authentication to secure access to different parts of your application.

## 🔹 Django's Built-in Permission System

Django provides a built-in permissions framework that includes:

- **Add** (`add_modelname`) ➡️ Allows adding new objects.
- **Change** (`change_modelname`) ➡️ Allows modifying existing objects.
- **Delete** (`delete_modelname`) ➡️ Allows deleting objects.
- **View** (`view_modelname`) ➡️ Allows viewing objects (added in Django 2.1).

Permissions are automatically created for each model when `makemigrations` and `migrate` are run.

### 1️⃣ Assigning Permissions to Users and Groups

#### 📝 Example: Assigning Permissions to a User

```python
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import MyModel

user = User.objects.get(username='john_doe')
content_type = ContentType.objects.get_for_model(MyModel)
permission = Permission.objects.get(codename='change_mymodel', content_type=content_type)

user.user_permissions.add(permission)
user.save()
```

#### 📝 Example: Assigning Permissions to a Group

```python
from django.contrib.auth.models import Group

group = Group.objects.create(name='Editors')
group.permissions.add(permission)
group.save()
```

## 🔐 Checking Permissions

Django provides multiple ways to check permissions in views and templates.

#### 📝 Example: Checking Permissions in Views

```python
from django.contrib.auth.decorators import permission_required

@permission_required('myapp.change_mymodel', raise_exception=True)
def my_view(request):
    return JsonResponse({'message': 'Permission granted'})
```

#### 📝 Example: Checking Permissions in Templates

```html
{% if user.has_perm('myapp.change_mymodel') %}
    <p>You have permission to edit this item.</p>
{% else %}
    <p>Editing is not allowed.</p>
{% endif %}
```

## 🛡️ Django REST Framework (DRF) Permissions

DRF provides an advanced permissions system for API views.

### 1️⃣ Default DRF Permissions

Set global permissions in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

### 2️⃣ Common DRF Permission Classes

- **AllowAny** ➡️ Grants unrestricted access.
- **IsAuthenticated** ➡️ Requires authentication.
- **IsAdminUser** ➡️ Grants access to admin users.
- **IsAuthenticatedOrReadOnly** ➡️ Allows read access to unauthenticated users.

#### 📝 Example: Applying Permissions to a View

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class SecureView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You have access'})
```

## ⚙️ Custom Permissions in DRF

For more control, define custom permissions.

#### 📝 Example: Creating a Custom Permission

```python
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user
```

Apply it to a view:

```python
class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
```

## 📌 Best Practices for Permissions

- ✅ **Use Django's built-in permission framework**
- ✅ **Leverage DRF permissions for APIs**
- ✅ **Assign permissions using groups for better management**
- ✅ **Check permissions at both model and view levels**
- ✅ **Use custom permissions when needed for fine-grained access control**

---

📖 This tutorial covers Django permissions, including built-in permissions, checking permissions, DRF permissions, and custom permissions. Implementing a robust permission system ensures security and proper access control in your application. 🚀
