import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "0") == "1"
ALLOWED_HOSTS = ["dev.usdm.com.ua", "usdm.com.ua", "www.usdm.com.ua", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://dev.usdm.com.ua",
    "https://usdm.com.ua",
    "https://www.usdm.com.ua",
]

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "site_content.apps.SiteContentConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "site_content.contact_rate_limit.ContactRateLimitMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "site_content.middleware.SiteLanguageMiddleware",
]
ROOT_URLCONF = "usdm_site.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "site_content.context_processors.language_navigation",
            "site_content.contact_form.contact_context",
        ],
    },
}]
WSGI_APPLICATION = "usdm_site.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": "postgres",
        "PORT": "5432",
    }
}

LANGUAGE_CODE = "uk"
LANGUAGES = [("uk", "Українська"), ("de", "Deutsch")]
SITE_LANGUAGES = ("uk", "de")
SITE_LANGUAGE_COOKIE_NAME = "usdm_language"
SITE_LANGUAGE_COOKIE_MAX_AGE = 365 * 24 * 60 * 60
SITE_PUBLIC_URL = "https://usdm.com.ua"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = "/srv/files/usdm/static" if not DEBUG else BASE_DIR / "static_collected"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/files/usdm/media" if not DEBUG else "/srv/dev-media/usdm"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_AGE = 10 * 60
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "website@usdm.com.ua")
CONTACT_RECIPIENT_EMAIL = os.environ.get("CONTACT_RECIPIENT_EMAIL", "sb@usdm.com.ua")
CONTACT_RATE_GUARD_URL = os.environ.get(
    "CONTACT_RATE_GUARD_URL",
    "http://contact-rate-guard:8080/check",
)
