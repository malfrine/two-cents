"""
Django settings for Two Cents project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ
import stripe
from mailchimp_marketing import Client

ROOT_DIR = environ.Path(__file__) - 3

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
    "whitenoise",
    "anymail",
]

LOCAL_APPS = ["core.apps.users", "core.apps.finances", "core.apps.payments"]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", default=True)
TESTING = env.bool("TESTING", default=False)
SECRET_KEY = env.str("SECRET_KEY")

# DOMAINS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
DOMAIN = env.str("DOMAIN", default="localhost")

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
if DEBUG:
    EMAIL_PORT = env.int("EMAIL_PORT", default="1025")
    EMAIL_HOST = env.str("EMAIL_HOST", default="mailhog")
else:
    EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
    ANYMAIL = {
        "SENDINBLUE_API_KEY": env.str("SENDINBLUE_API_KEY"),
    }

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("Malfrine Das", "malfrine@ualberta.ca"),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
engine = (
    "django.db.backends.postgresql_psycopg2"
    if DEBUG
    else "django.db.backends.postgresql"
)

DATABASES = {
    "default": {
        "ENGINE": engine,
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST", default="postgres"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
    },
}

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str("/staticfiles")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/staticfiles/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str("staticfiles"),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# white noise compression spec
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str("/media")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "core.config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "core.config.wsgi.application"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": STATICFILES_DIRS,
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"


# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "UPLOADED_FILES_USE_URL": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.firebase.authentication.FirebaseAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
}


# raven sentry client
# See https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ["raven.contrib.django.raven_compat"]
RAVEN_MIDDLEWARE = [
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware"
]
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

# Sentry Configuration
SENTRY_DSN = "" if DEBUG else env.str("SENTRY_DSN", "")
SENTRY_CLIENT = "raven.contrib.django.raven_compat.DjangoClient"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARN", "handlers": ["sentry"]},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s (%(filename)s:%(lineno)s)"
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "DEBUG",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "sentry"],
            "propagate": False,
        },
    },
}

RAVEN_CONFIG = {"DSN": SENTRY_DSN}

# Hashid Field Settings
HASHID_FIELD_ALLOW_INT_LOOKUP = True
HASHID_FIELD_SALT = env.str("DJANGO_HASHID_FIELD_SALT")

# Stripe
IS_STRIPE_TEST = env.bool("STRIPE_TEST", True)
if IS_STRIPE_TEST:
    STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_TEST_PUBLISHABLE_KEY", "")
    STRIPE_SECRET_KEY = env.str("STRIPE_TEST_SECRET_KEY", "")
else:
    STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PROD_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = env.str("STRIPE_PROD_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env.str("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = STRIPE_SECRET_KEY
stripe = stripe

# Mailchimp
mailchimp = Client()
mailchimp.set_config(
    {
        "api_key": env.str("MAILCHIMP_API_KEY"),
        "server": env.str("MAILCHIMP_SERVER_PREFIX"),
    }
)
TWO_CENTS_AUDIENCE_ID = "f4b38887b5"
