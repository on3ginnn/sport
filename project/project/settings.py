import os
import pathlib

import django.urls
from django.utils.translation import gettext_lazy as _
import dotenv


__all__ = []

dotenv.load_dotenv()


def true_load(value: str, defoult: bool) -> bool:
    env_value = os.getenv(value, str(defoult)).lower()
    return env_value in ("", "true", "yes", "1", "y")


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "ABOBA")

DEBUG = true_load("DJANGO_DEBUG", False)

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest@localhost:5672//")

DEFAULT_USER_IS_ACTIVE = true_load("DJANGO_DEFAULT_USER_IS_ACTIVE", DEBUG)

ALLOWED_HOSTS = list(
    map(str.strip, os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")),
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "about.apps.AboutConfig",
    "users.apps.UsersConfig",
    "homepage.apps.HomepageConfig",
    "feedback.apps.FeedbackConfig",
    "streetsport.apps.StreetsportConfig",
    "djcelery_email",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("PG_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("PG_DB_NAME", "myproject"),
        "USER": os.getenv("PG_USER", "myprojectuser"),
        "PASSWORD": os.getenv("PG_PASSWORD", "password"),
        "HOST": os.getenv("PG_HOST", "localhost"),
        "PORT": os.getenv("PG_PORT", "5432"),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth." "password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.NumericPasswordValidator"
        ),
    },
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = os.getenv("DJANGO_INTERNAL_IPS", "127.0.0.1").split(",")

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["users.backends.EmailUsernameBackend"]

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

LOCALE_PATHS = (BASE_DIR / "locale",)

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOGIN_URL = django.urls.reverse_lazy("users:login")
LOGIN_REDIRECT_URL = django.urls.reverse_lazy("homepage:main")
LOGOUT_REDIRECT_URL = django.urls.reverse_lazy("homepage:main")

STATIC_ROOT = BASE_DIR.parent / "static"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.yandex.ru")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = true_load("EMAIL_USE_SSL", True)

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "Damir.DeBug@yandex.ru")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "aukqrygbsvpogpbs")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER


CELERY_BROKER_URL = AMQP_URL
