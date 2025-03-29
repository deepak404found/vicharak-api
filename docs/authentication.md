# Django Authentication Tutorial

Authentication is a crucial part of any web application, ensuring secure access to resources. Django provides built-in authentication mechanisms that can be extended for custom authentication needs.

## 🔹 Django's Built-in Authentication System

Django comes with an authentication system that includes user authentication, sessions, and permissions.

### 1️⃣ User Authentication

Django provides the `User` model to handle user-related information.

#### 📝 Example: Creating a User

```python
from django.contrib.auth.models import User

user = User.objects.create_user(username='john_doe', password='securepassword')
user.save()
```

### 2️⃣ Login and Logout

#### 📝 Example: Logging in a User

```python
from django.contrib.auth import authenticate, login

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)
```

#### 📝 Example: Logging out a User

```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
```

## 🔐 Authentication Backends

Django allows using different authentication backends to support custom authentication.

### 📝 Example: Custom Authentication Backend

```python
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

## 🛡️ Django REST Framework (DRF) Authentication

Django REST Framework (DRF) provides multiple authentication methods.

### 1️⃣ Token Authentication

#### 📝 Example: Enabling Token Authentication

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SecureViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

### 2️⃣ JWT Authentication (via `djangorestframework-simplejwt`)

#### 📝 Example: Setting Up JWT Authentication

Install the package:

```sh
pip install djangorestframework-simplejwt
```

Update `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

#### 📝 Example: Generating a JWT Token

```python
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

### SimpleJWT Views

SimpleJWT provides views for obtaining and refreshing tokens.

```python
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
```

## ⚙️ Custom Authentication Classes

You can create custom authentication classes by extending `BaseAuthentication`.

### 📝 Example: Custom Authentication Class

For example, you can create a custom authentication class that checks for a specific header in the request.

```python
from rest_framework.authentication import BaseAuthentication

class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        custom_header = request.headers.get('X-Custom-Header')
        if custom_header == 'expected_value':
            return (None, None)  # Return user and auth token
        return None  # Authentication failed
```

Use this custom authentication class in your views:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .authentication import CustomHeaderAuthentication

class CustomAuthView(APIView):
    authentication_classes = [CustomHeaderAuthentication]

    def get(self, request):
        return Response({'message': 'Authenticated with custom header!'}, status=status.HTTP_200_OK)
```

## 🔒 Securing APIs with DRF

To secure your APIs, you can use various authentication and permission classes provided by DRF.

### 1️⃣ Permission Classes

DRF provides built-in permission classes to control access to your API views.

#### 📝 Example: Using Permission Classes

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({'message': 'Hello Admin!'}, status=status.HTTP_200_OK)
```

## 📌 Best Practices for Authentication

- ✅ **Use Django's built-in authentication whenever possible**
- ✅ **Enforce strong password policies**
- ✅ **Use `AUTH_USER_MODEL` for custom user fields**
- ✅ **Enable secure authentication methods like JWT**
- ✅ **Store authentication tokens securely**
- ✅ **Use HTTPS to encrypt authentication data**

---

📖 This tutorial covers Django authentication, from user management to authentication backends and securing APIs using DRF. Implementing robust authentication ensures your application remains secure and reliable.

[🔙 Back to Main Docs](./README.md)
