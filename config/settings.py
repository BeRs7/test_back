from datetime import timedelta
from pathlib import Path
import environ
import os
from django.utils.translation import gettext_lazy as _
from config.celery import *  # noqa
from config.celerybeat import *  # noqa


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(str(BASE_DIR / ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value("SECRET_KEY", default="random")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
SITE_ID = 1

# Application definition

DJANGO_APPS = [
    "clearcache",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "drf_yasg",
    "rest_framework",
    "knox",
    "parler",
    "sorl.thumbnail",
    "solo",
    "djcelery_email",
    "django_filters",
    "mptt",
    "cachalot",
    "fieldsignals",
    "searchableselect",
    "ckeditor",
    "ckeditor_uploader",
    "colorfield",
    "corsheaders",
]

LOCAL_APPS = [
    "config",
    "users",
    "catalog",
    "utils",
    "orders",
    "cart",
    "subscriptions",
    "crm",
    "text_pages",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.SaveClientIPMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ru"

LANGUAGES = [("ru", _("Russian")), ("en", _("English"))]

LOCALE_PATHS = (os.path.join(ROOT_DIR, "locale"),)

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DEBUG TOOLBAR

if DEBUG:

    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "cachalot.panels.CachalotPanel",
    ]
else:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_HOST = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else:
#     CELERY_EMAIL_TASK_CONFIG = {
#         "queue": "default",
#     }
#     EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = str(BASE_DIR / "media")
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR / "static")]

FILE_UPLOAD_PERMISSIONS = 0o644
THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.redis_kvstore.KVStore"
# THUMBNAIL_REDIS_HOST = env.str("THUMBNAIL_REDIS_HOST")
# LANGS
PARLER_ENABLE_CACHING = False
CORS_ALLOW_ALL_ORIGINS = True

# set site id
PARLER_LANGUAGES = {
    1: ({"code": "ru"}, {"code": "en"}),
    "default": {
        "fallback": "ru",  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        "hide_untranslated": False,  # the default; let .active_translations() return fallbacks too.
    },
}
REDIS_URL = 'redis://127.0.0.1:6379'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}
SELECT2_CACHE_BACKEND = "select2"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 999999

# CELERY
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_QUEUE = CELERY_DEFAULT_QUEUE
CELERY_TASK_ROUTES = {
    "orders.tasks.email.send_created_order_information": {"queue": "default"},
}

EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
# SERVER_EMAIL = env.str("SERVER_EMAIL")
# EMAIL_HOST = env.str("EMAIL_HOST")
# EMAIL_PORT = env.int("EMAIL_PORT")
# EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "knox.auth.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
    ],
}
REST_KNOX = {
    "TOKEN_TTL": timedelta(days=28),
    "USER_SERIALIZER": "users.serializers.MiddleUserSerializer",
    "AUTO_REFRESH": True,
    "TOKEN_LIMIT_PER_USER": float("inf"),
    "MIN_REFRESH_INTERVAL": 3600,
}

# CKEDITOR
CKEDITOR_UPLOAD_PATH = "content/ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        "filebrowserUploadUrl": "/crm/ckeditor/upload/",
        "filebrowserBrowseUrl": "/crm/ckeditor/browse/",
        "toolbar": [
            ["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
            [
                "NumberedList",
                "BulletedList",
                "Indent",
                "Outdent",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
                "Table",
            ],
            ["Image", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"],
            ["Undo", "Redo"],
            ["Source"],
            ["Maximize"],
        ],
        "height": 300,
        "width": 650,
    },
}

# DOMAIN = env.str("DOMAIN")
# SITE_DOMAIN = env.str("SITE_DOMAIN")
# FRONTEND_DOMAIN = env.str("FRONTEND_DOMAIN")

# YCLIENTS_TOKEN = env.str("YCLIENTS_TOKEN")
# YCLIENTS_COMPANY_ID = env.str("YCLIENTS_COMPANY_ID")
# YCLIENTS_FORM_ID = env.str("YCLIENTS_FORM_ID")
# YCLIENTS_STAFF_ID = env.str("YCLIENTS_STAFF_ID")

