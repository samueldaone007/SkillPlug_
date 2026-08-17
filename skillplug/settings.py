"""
SkillPlug - Nigerian Student Skills Marketplace
Django settings for production and development environments.
"""
 
from pathlib import Path
from decouple import config
import os
 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
# =============================================================================
# CORE SETTINGS
# =============================================================================
 
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")
 
DEBUG = config("DEBUG", default=True, cast=bool)
 
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)
 
 
# =============================================================================
# APPLICATION DEFINITION
# =============================================================================
 
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    
    # Third-party
    "crispy_forms",
    "crispy_tailwind",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_htmx",
    
    # Local apps
    "apps.accounts",
    "apps.marketplace",
    "apps.jobs",
    "apps.reviews",
]
 
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]
 
ROOT_URLCONF = "skillplug.urls"
 
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.marketplace.context_processors.marketplace_stats",
            ],
        },
    },
]
 
WSGI_APPLICATION = "skillplug.wsgi.application"
ASGI_APPLICATION = "skillplug.asgi.application"
 
 
# =============================================================================
# DATABASE
# =============================================================================
 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
 
 
# =============================================================================
# AUTHENTICATION & ALLAUTH
# =============================================================================
 
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
 
AUTH_USER_MODEL = "accounts.User"
 
# django-allauth settings
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_SIGNUP_REDIRECT_URL = "profile_create"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
 
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "account_login"
 
# Password validation
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
 
 
# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
 
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True
 
 
# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================
 
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
 
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
 
 
# =============================================================================
# CRISPY FORMS
# =============================================================================
 
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
 
 
# =============================================================================
# EMAIL SETTINGS
# =============================================================================
 
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)
 
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@skillplug.ng")
 
 
# =============================================================================
# MESSAGES
# =============================================================================
 
from django.contrib.messages import constants as messages
 
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}
 
 
# =============================================================================
# SECURITY
# =============================================================================
 
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
 
 
# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================
 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
 
 
# =============================================================================
# WHATSAPP SETTINGS
# =============================================================================
 
WHATSAPP_DEFAULT_MESSAGE = config(
    "WHATSAPP_DEFAULT_MESSAGE",
    default="Hello! I found you on SkillPlug and I'm interested in your services.",
)