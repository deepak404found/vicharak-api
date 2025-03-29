# 🚢 Deploying Django Rest Framework (DRF) APIs

Deploying a Django Rest Framework (DRF) API requires careful planning to ensure security, scalability, and performance. This guide covers best practices for deploying DRF applications.

---

## 🆚 Difference Between `os.getenv` and `dotenv`

- `os.getenv("VAR_NAME", "default_value")`: Retrieves environment variables as strings and requires manual type conversion.
- `dotenv` (`python-dotenv`): Loads environment variables from a `.env` file into the runtime environment automatically, making local development easier.

---

## 1️⃣ Preparing for Deployment

Before deploying, ensure that your DRF application is production-ready by following these steps:

### ✅ Environment Setup

- Use **virtual environments** to manage dependencies (`venv` or `pipenv`).
- Use **environment variables** to store sensitive data (e.g., database credentials, secret keys).
- Set `DEBUG = False` in `settings.py`.
- Use `.env` files for better environment management:

  ```python
  from dotenv import load_dotenv
  import os
  
  load_dotenv()
  
  DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
  SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")
  DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
  ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
  CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
  ```

  This ensures security by keeping secrets out of source code.

### ✅ Database Configuration

- Use a production-ready database like **PostgreSQL** or **MySQL**.
- Run database migrations before deployment (`python manage.py migrate`).
- Use a connection pooler like **PgBouncer** for PostgreSQL.

### ✅ Static & Media Files

- Use **WhiteNoise** for serving static files (`pip install whitenoise`).
- Store media files in **cloud storage** (AWS S3, Google Cloud Storage, etc.).
- Run `python manage.py collectstatic` before deployment.

### ✅ Security Best Practices

- Set `ALLOWED_HOSTS` to restrict access to known domains.
- Use **HTTPS** with an SSL certificate.
- Set up **CORS** properly (`django-cors-headers`).
- Protect against SQL injection, CSRF, and XSS attacks.
- Use **Django security middleware** (`SECURE_*` settings).

---

## 2️⃣ Choosing a Deployment Method

There are multiple ways to deploy a DRF application. Here are some common options:

### 🌐 Cloud Providers

- **AWS EC2 / Lambda**: Scalable deployment options.
- **Google Cloud App Engine**: Serverless deployment.
- **Azure App Service**: Easy integration with Microsoft ecosystem.
- **DigitalOcean / Linode / Vultr**: Budget-friendly VPS hosting.

### 🐳 Containerized Deployment

- Use **Docker** to package your application (`Dockerfile`).
- Deploy with **Docker Compose** (`docker-compose.yml`).
- Use **Kubernetes** for scalable deployment.

### 🔧 Platform-as-a-Service (PaaS)

- **Heroku**: Easy to use (`git push heroku main`).
- **Railway.app / Render**: Simple and cost-effective alternatives.
- **PythonAnywhere**: Python-specific deployment.

### 🌍 Traditional Deployment

- Deploy on a **Linux VPS** (Ubuntu, Debian, etc.).
- Use **Gunicorn** + **Nginx** for running the application.
- Manage processes with **Supervisor** or **systemd**.

---

## 3️⃣ Deployment Steps

### 🏗 1. Install Production Dependencies

```sh
pip install -r requirements.txt
```

### 🔑 2. Configure Environment Variables

Use `.env` files or system environment variables:

```sh
export DJANGO_SECRET_KEY='your-secret-key'
export DATABASE_URL='postgres://user:password@host:port/dbname'
```

### 🚀 3. Run Migrations

```sh
python manage.py migrate
```

### 🏞 4. Collect Static Files

```sh
python manage.py collectstatic --noinput
```

### 🌐 5. Start Application (Gunicorn Example)

```sh
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

### 🛠 6. Set Up Reverse Proxy (Nginx Example)

Create an Nginx configuration file:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 🏎 7. Enable Process Manager (Supervisor Example)

```ini
[program:gunicorn]
command=/path/to/venv/bin/gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn.err.log
stdout_logfile=/var/log/gunicorn.out.log
```

---

## 4️⃣ Scaling & Monitoring

### 📈 Load Balancing

- Use **Nginx** or **HAProxy** to distribute traffic.
- Implement **horizontal scaling** with multiple instances.

### 🔥 Performance Optimization

- Enable **database indexing**.
- Use **caching** (Redis, Memcached).
- Optimize queries using Django’s **select_related** and **prefetch_related**.

### 👀 Monitoring & Logging

- Use **Sentry** for error tracking.
- Enable **logging** with Django’s built-in logging system.
- Monitor server performance using **Prometheus + Grafana**.

---

## ✅ Conclusion

By following these best practices, you can successfully deploy a DRF API in a production environment with security, scalability, and high performance in mind. 🚀
