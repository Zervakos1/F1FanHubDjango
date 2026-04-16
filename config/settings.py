"""
Django settings for the config project.

This file contains:
- environment-based configuration
- installed apps and middleware
- database setup for local SQLite or deployed PostgreSQL
- static and media file settings
- production security settings for deployment platforms like Render
"""

import os
from pathlib import Path

import dj_database_url

# Base directory of the Django project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key used by Django for cryptographic signing.
# In production, this should always come from environment variables.
SECRET_KEY = os.getenv("SECRET_KEY", "local-dev-secret-key-change-me")

# Debug mode is enabled only when DJANGO_DEBUG is explicitly set to "True".
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Allowed hosts for local development and deployment.
# Render automatically provides the deployed hostname through environment variables.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS += [host.strip() for host in extra_hosts.split(",") if host.strip()]

# Trusted origins for CSRF protection in deployed environments.
CSRF_TRUSTED_ORIGINS = []

render_external_url = os.getenv("RENDER_EXTERNAL_URL")
if render_external_url:
    CSRF_TRUSTED_ORIGINS.append(render_external_url)

extra_csrf = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "")
if extra_csrf:
    CSRF_TRUSTED_ORIGINS += [origin.strip() for origin in extra_csrf.split(",") if origin.strip()]

# Applications installed in this project.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "catalog",
    "cart",
    "reviews",
    "dashboard",
]

# Middleware stack for security, sessions, CSRF, authentication, and messages.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL configuration file.
ROOT_URLCONF = "config.urls"

# Template engine configuration.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application entry point for deployment.
WSGI_APPLICATION = "config.wsgi.application"

# Database configuration.
# Uses PostgreSQL in deployment when DATABASE_URL is provided.
# Falls back to local SQLite for development.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# Password validation rules for user accounts.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization and timezone settings.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Athens"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images).
# WhiteNoise is used to serve static files in production.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Uploaded media files.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# End user session when the browser closes.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Extra security settings enabled only in production.
if not DEBUG:
    # Tell Django to trust the X-Forwarded-Proto header from the proxy.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Force HTTPS in production.
    SECURE_SSL_REDIRECT = True

    # Secure cookies over HTTPS only.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # HTTP Strict Transport Security settings.
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Additional browser security headers.
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"