import os

# Import all settings from template first
from .settings_template import *  # NOQA ignore=F405
from .settings_template import INSTALLED_APPS

# Enable DEBUG mode to use development static file serving
DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

INSTALLED_APPS += ["django_opensearch_dsl"]

# Override STATICFILES_FINDERS to remove npm finder that's causing crashes
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# IMPORTANT: Override STORAGES AFTER importing template to ensure it takes precedence
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "assets": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "visualizations": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Also set the old-style setting for compatibility
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Globally disable auto-syncing
OPENSEARCH_DSL_AUTOSYNC = os.getenv("OPENSEARCH_DSL_AUTOSYNC", False)

OPENSEARCH_DSL = {
    "default": {"hosts": os.getenv("OPENSEARCH_ENDPOINT", "9200:9200")},
    "secure": {
        "hosts": [
            {"scheme": "https", "host": os.getenv("OPENSEARCH_ENDPOINT"), "port": 9201}
        ],
        "http_auth": ("admin", os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "")),
        "timeout": 120,
    },
}


# HMAC activation flow provide the two-step registration process,
# the user signs up and then completes activation via email instructions.

# This is *not* a secret for the HMAC activation workflow — see:
# https://django-registration.readthedocs.io/en/2.0.4/hmac.html#security-considerations
REGISTRATION_SALT = "django_registration"

RATELIMIT_BLOCK = os.getenv("RATELIMIT_BLOCK", "").lower() not in ("false", "0")
