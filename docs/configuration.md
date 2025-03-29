# ⚙️ Django & DRF Settings Configuration

This document provides an overview of `settings.py` configurations, including Django settings and DRF environment variables to enhance API functionality. It also includes best practices and explanations for each setting.

---

## 🏗 1. Basic Django Settings

### Debug Mode

```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
```

**Why?**

- Debug mode should be disabled in production to prevent sensitive error details from being exposed.
- Using `.env` ensures the setting is configurable without modifying code.

### Secret Key Management

```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret")
```

**Why?**

- A secret key is crucial for Django’s security mechanisms.
- Storing it in `.env` prevents exposure in version control.

### Allowed Hosts

```python
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
```

**Why?**

- Restricts which domains can access your Django app, preventing security risks like Host Header Attacks.

---

## 📌 2. Django Rest Framework (DRF) Settings

### Default Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Why?

- **Authentication**: Ensures secure API access using tokens and sessions.
- **Permissions**: Restricts API usage to authenticated users.
- **Pagination**: Prevents performance issues from large query results.

### CORS Configuration

```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
```

**Why?**

- Enables cross-origin requests (CORS), allowing frontend applications hosted on different domains to interact with the backend securely.

---

## 🔄 3. Database Configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mydatabase'),
        'USER': os.getenv('DB_USER', 'user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**Why?**

- Separating credentials from code improves security.
- PostgreSQL is preferred for production due to better scalability and performance over SQLite.

---

## 🚀 4. Additional DRF Features

### API Throttling

```python
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle',
]
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/day',
    'user': '1000/day',
}
```

**Why?**

- Limits API requests to prevent abuse and protect server resources.

### Versioning

```python
REST_FRAMEWORK['DEFAULT_VERSIONING_CLASS'] = 'rest_framework.versioning.NamespaceVersioning'
```

**Why?**

- Allows handling multiple API versions without breaking existing clients.

### Exception Handling

```python
REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'myapp.exceptions.custom_exception_handler'
```

**Why?**

- Custom error responses improve debugging and user experience.

### Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

**Why?**

- Helps track errors, monitor system health, and debug efficiently.

---

## ✅ Conclusion

This guide ensures a scalable, secure, and well-structured Django + DRF configuration. Keep your `.env` secure and update settings as your project evolves. 🚀

[🔙 Back to Main Docs](./README.md)
