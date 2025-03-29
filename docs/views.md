# Django Views Tutorial

Django views are responsible for handling requests and returning responses. Views act as the business logic layer, processing user input, interacting with the database, and rendering templates or returning API responses.

For more information on Django views, refer to the official documentation: [Django Views Documentation](https://docs.djangoproject.com/en/stable/topics/http/views/).

## 📂 Example

Here’s are some examples of how you can use views in a Django project:

- **[`vichar/views.py`](../vichar/views.py)**
- **[`user/views.py`](../user/views.py)**

## 📖 Overview of Django Views

Django views can be categorized into several types, each serving different purposes. The main types of views in Django are:

1. **Function-Based Views (FBVs)**: Simple Python functions that handle requests and return responses.
2. **Class-Based Views (CBVs)**: Object-oriented views that provide more structure and reusability.
3. **ViewSets**: Used in Django REST Framework (DRF) to create RESTful APIs efficiently.
4. **APIView**: A class-based view for building APIs with DRF.
5. **Generic Views**: Built-in views provided by Django for common tasks like displaying lists or details of objects.
6. **Mixins**: Reusable components that can be combined to create custom views.
7. **Action-Based Views**: Custom actions defined in viewsets for specific functionalities.

## 🔹 Types of Views in Django

### 1️⃣ Function-Based Views (FBVs)

FBVs are simple Python functions that receive an HTTP request and return an HTTP response.

#### 📝 Example: Retrieving Vichars

```python
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Vichar

@login_required
def list_vichars(request):
    vichars = Vichar.objects.filter(owner=request.user)
    data = {"vichars": list(vichars.values())}
    return JsonResponse(data)
```

Usage of decorators like `@login_required` ensures that only authenticated users can access the view.

Usage:

Once the view is defined, you can map it to a URL in your `urls.py`:

```python
from django.urls import path
from .views import list_vichars
urlpatterns = [
    path('vichars/', list_vichars, name='list_vichars'),
]
```

### 2️⃣ Class-Based Views (CBVs)

CBVs provide reusable, structured views using Django’s built-in classes.

#### 📝 Example: Using Django's `ListView` to Display Vichars

```python
from django.views.generic import ListView
from .models import Vichar

class VicharListView(ListView):
    model = Vichar
    template_name = "vichar_list.html"
    context_object_name = "vichars"

    def get_queryset(self):
        return Vichar.objects.filter(owner=self.request.user)
```

Usage:
To use the `VicharListView`, you need to map it to a URL in your `urls.py`:

```python
from django.urls import path
from .views import VicharListView

urlpatterns = [
    path('vichars/', VicharListView.as_view(), name='vichar_list'),
]
```

### 3️⃣ ViewSets (for Django REST Framework)

ViewSets are used in DRF to create RESTful APIs efficiently. They combine multiple views (list, retrieve, create, update, delete) into a single class.

#### 📝 Example: `VicharViewSet` for Managing Vichars

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vichar
from .serializers import VicharSerializer

class VicharViewSet(viewsets.ModelViewSet):
    serializer_class = VicharSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vichar.objects.filter(owner=self.request.user)
```

Usage:
To use the `VicharViewSet`, you need to register it with a router in your `urls.py`:

```python
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import VicharViewSet
router = DefaultRouter()
router.register(r'vichars', VicharViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 4️⃣ API Views (for Django REST Framework)

API views are function-based views specifically designed for building APIs with DRF. They provide more control over the request and response process.

#### 📝 Example: Creating a Vichar API View

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vichar
from .serializers import VicharSerializer

class VicharAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vichars = Vichar.objects.filter(owner=request.user)
        serializer = VicharSerializer(vichars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VicharSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

Usage:

To use the `VicharAPIView`, you need to map it to a URL in your `urls.py`:

```python
from django.urls import path
from .views import VicharAPIView
urlpatterns = [
    path('api/vichars/', VicharAPIView.as_view(), name='vichar_api'),
]
```

### 5️⃣ Generic Views

Generic views are a set of built-in views provided by Django that handle common tasks like displaying lists or details of objects. They are built on top of CBVs and provide a lot of functionality out of the box.

#### 📝 Example: Using `DetailView` to Display Vichar Details

```python
from django.views.generic import DetailView
from .models import Vichar
class VicharDetailView(DetailView):
    model = Vichar
    template_name = "vichar_detail.html"
    context_object_name = "vichar"

    def get_queryset(self):
        return Vichar.objects.filter(owner=self.request.user)
```

Usage:
To use the `VicharDetailView`, you need to map it to a URL in your `urls.py`:

```python
from django.urls import path
from .views import VicharDetailView
urlpatterns = [
    path('vichars/<int:pk>/', VicharDetailView.as_view(), name='vichar_detail'),
]
```

### 6️⃣ Mixins

Mixins are a way to add reusable functionality to your views. They allow you to create custom views by combining different behaviors.

#### 📝 Example: Using `CreateModelMixin` to Add Create Functionality

```python
from rest_framework import mixins, viewsets
from .models import Vichar
from .serializers import VicharSerializer
class VicharCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vichar.objects.all()
    serializer_class = VicharSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

Usage:
To use the `VicharCreateView`, you need to map it to a URL in your `urls.py`:

```python
from django.urls import path
from .views import VicharCreateView
urlpatterns = [
    path('api/vichars/create/', VicharCreateView.as_view({'post': 'create'}), name='vichar_create'),
]
```

### 7️⃣ Action-Based Views

Action-based views are a way to define custom actions in your viewsets. They allow you to create additional endpoints for specific actions.

#### 📝 Example: Adding a Custom Action to `VicharViewSet`

```python
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets, filters
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Vichar
from .serializers import VicharSerializer

class VicharViewSet(
    mixins.ListModelMixin,  # GET list
    mixins.RetrieveModelMixin,  # GET detail
    mixins.CreateModelMixin,  # POST
    mixins.UpdateModelMixin,  # PUT/PATCH
    mixins.DestroyModelMixin,  # DELETE
    viewsets.GenericViewSet,
):
    queryset = Vichar.objects.all()
    serializer_class = VicharSerializer
    permission_classes = [IsAuthenticated]

    # Action to get deleted vichars
    @action(detail=False, methods=["get"])
    def list_deleted(self, request):
        queryset = Vichar.objects.filter(deleted_at__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

Explanation:

- `@action`: This decorator allows you to define custom actions in your viewset. The `detail` parameter indicates whether the action is for a single object or a list.

Usage:
To use the `list_deleted` action, you can access it via the URL `/api/vichars/list_deleted/`.

```python
from django.urls import path
from .views import VicharViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vichars', VicharViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## 🔐 Authentication and Permissions

### 🔑 Enforcing Authentication in Views

Django REST Framework provides built-in authentication classes to protect views.

#### 📝 Example: Protecting Vichars API with Token Authentication

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SecureVicharViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

### ⚙️ Using Custom Permissions

Custom permissions allow defining access control logic beyond simple authentication.

#### 📝 Example: Restricting Vichar Access to Owners Only

```python
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

🔹 Applying this permission in a view:

```python
class VicharDetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

## 📌 Best Practices for Django Views

- ✅ **Use CBVs when possible**: They provide reusable and maintainable code.
- ✅ **Use DRF ViewSets for APIs**: They simplify API management.
- ✅ **Implement proper authentication and permissions**: Ensure data security.
- ✅ **Use decorators for FBVs**: `@login_required` or `@permission_required` enhances security.
- ✅ **Keep views clean**: Move complex logic to services or managers.

---
📖 This tutorial covers the fundamentals of Django views, from function-based to class-based views and API viewsets, with practical examples from Vicharak. Mastering views helps build efficient Django applications.

[🔙 Back to Main Docs](./README.md)
