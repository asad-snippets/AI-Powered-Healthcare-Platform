import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-…"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Custom Idle Timeout Middleware
    "home.middleware.IdleTimeoutMiddleware",
]

ROOT_URLCONF = "health.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "health.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aihealthcare",
        "USER": "root",
        "PASSWORD": "asad1234",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom authentication backend
AUTHENTICATION_BACKENDS = [
    "home.auth_backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "/Login/"

# ─── Session Cookie Settings ────────────────────────────────────────────────
# Adjust session timeout to 300 seconds (5 minutes), matching the comment
SESSION_COOKIE_AGE = 300  # Timeout after 5 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Reset the session timeout on every request

# Ensure the session expires when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security flags - set to True if using HTTPS
SESSION_COOKIE_SECURE = False if DEBUG else True  # Set to False in dev mode, True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent access to cookies via JavaScript
SESSION_COOKIE_SAMESITE = "Lax"  # Adjust as per your needs

# ─────────────────────────────────────────────────────────────────────────────
