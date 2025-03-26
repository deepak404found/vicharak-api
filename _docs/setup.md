# 🌟 Introduction to Django Rest Framework (DRF)

Django Rest Framework (DRF) is an open-source framework for building Web APIs with Django. It provides robust tools for authentication, serialization, permissions, and views, making API development seamless and efficient. With a browsable API feature, DRF simplifies debugging and testing.

### ✨ Key Features of DRF

- **🔄 Serialization**: Converts complex data types into JSON.
- **🔐 Authentication & Permissions**: Supports Token, JWT, and custom authentication.
- **🛠️ Viewsets & Routers**: Simplifies URL configuration.
- **🌐 Browsable API**: Interactive API documentation.
- **📊 Throttling & Pagination**: Helps manage large datasets and rate limits.

## ⚙️ Installation using Poetry

To install Django and DRF using Poetry, follow these steps:

1. **Initialize a Poetry project** (if not already set up):

    Install Poetry using `curl`:

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Add Poetry to your PATH:

    ```sh
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    ```bash
    poetry init
    ```

2. **➕ Add dependencies:**

    ```bash
    poetry add django djangorestframework djangorestframework-simplejwt
    ```

### 🚀 Setting up a Django project with DRF

Setting up a new Django project with DRF involves creating a new project, starting an app, configuring settings, and running migrations. Here's a step-by-step guide:

1. **📂 Create a new Django project:**

    ```bash
    poetry run django-admin startproject myproject 
    cd myproject

    #or 

    poetry run django-admin startproject myproject .
    ```

2. **📦 Start a new Django app:**

    ```bash
    poetry run python manage.py startapp api
    ```

3. **🛠️ Add applications to `INSTALLED_APPS` in `settings.py`:**

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'rest_framework',
        'rest_framework_simplejwt',

        # Add your app here
        'api',
    ]
    ```

4. **⚙️ Add `rest_framework` and `rest_framework_simplejwt` settings to `settings.py`:**

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }
    ```

5. **📥 Run migrations:**

    Before running the migrations, make sure to make migrations for the `api` app:

    ```bash
    poetry run python manage.py makemigrations api
    poetry run python manage.py migrate
    ```

6. **👤 Create a superuser:**

    ```bash
    poetry run python manage.py createsuperuser
    ```

7. **▶️ Run the development server:**

    ```bash
    poetry run python manage.py runserver
    ```

🎉 Now, the basic DRF setup with Simple JWT authentication is completed!