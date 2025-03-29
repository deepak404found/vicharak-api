# 🚦 Throttling in Django Rest Framework (DRF)

## 🔍 What is Throttling?

Throttling is a technique used to control the rate of requests a client can make to an API. It helps in preventing abuse, reducing server load, and ensuring fair usage of resources. In Django Rest Framework (DRF), throttling is a built-in feature that can be easily configured.

## 📌 Why Use Throttling?

- Prevent **API abuse** by limiting excessive requests from users.
- Protect **server resources** from overload.
- Ensure **fair usage** among multiple users.
- Enhance **security** by limiting brute-force attacks.

## ⚙️ Types of Throttling in DRF

DRF provides different types of throttling classes:

1. **AnonRateThrottle** – Limits requests from anonymous users.
2. **UserRateThrottle** – Limits requests from authenticated users.
3. **ScopedRateThrottle** – Limits requests based on a defined scope.
4. **Custom Throttle Classes** – Allows defining custom throttling logic.

## 🛠️ Configuring Throttling in DRF

Throttling can be enabled and configured in the **`settings.py`** file of your Django project:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',  # Limit anonymous users to 10 requests per minute
        'user': '100/day'     # Limit authenticated users to 100 requests per day
    }
}
```

## 🔄 How Throttling Works

When a request is made, DRF checks the defined throttling rules:

- If the request exceeds the limit, **HTTP 429 Too Many Requests** is returned.
- Otherwise, the request proceeds as normal.

## 🎯 Using Scoped Throttling

Scoped throttling is useful for limiting requests on a per-view basis. Example:

```python
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response

class ExampleView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'example_scope'

    def get(self, request):
        return Response({"message": "Hello, World!"})
```

Define scope in **`settings.py`**:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'example_scope': '5/minute',
    }
}
```

## 🏗️ Creating Custom Throttle Classes

You can create a custom throttle class by extending `BaseThrottle`:

```python
from rest_framework.throttling import BaseThrottle
from datetime import datetime, timedelta

class CustomThrottle(BaseThrottle):
    def __init__(self):
        self.history = {}

    def allow_request(self, request, view):
        user_ip = self.get_ident(request)
        now = datetime.now()
        self.history.setdefault(user_ip, []).append(now)
        self.history[user_ip] = [t for t in self.history[user_ip] if now - t < timedelta(minutes=1)]
        return len(self.history[user_ip]) <= 5  # Limit: 5 requests per minute
```

## 🚀 Summary

- **Throttling** controls API request rates.
- **DRF provides built-in throttling classes** (Anon, User, Scoped).
- **Can be configured globally** in `settings.py`.
- **Custom throttling** allows more flexibility.

This helps maintain API security, fairness, and performance. ✅

---
💡 *Next:* Learn about **Testing in DRF** 🧪

[🔙 Back to Main Docs](./README.md)
