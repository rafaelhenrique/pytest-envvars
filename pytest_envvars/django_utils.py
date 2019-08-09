"""
This module is based on pytest-django project.
Reference: https://github.com/pytest-dev/pytest-django
"""

import os
import sys
from pathlib import Path


def is_django_project():
    """Return False when is not a Django project"""
    if django_settings_is_configured():
        return True

    for manage_file in Path().rglob("manage.py"):
        if not manage_file.is_file():
            continue

        with open(manage_file) as manage_buffer:
            for line in manage_buffer:
                if 'from django' in line or 'import django' in line:
                    return True
    return False


def django_settings_is_configured():
    """Return whether the Django settings module has been configured.

    This uses either the DJANGO_SETTINGS_MODULE environment variable, or the
    configured flag in the Django settings object if django.conf has already
    been imported.
    """
    ret = bool(os.environ.get("DJANGO_SETTINGS_MODULE"))

    if not ret and "django.conf" in sys.modules:
        return sys.modules["django.conf"].settings.configured

    return ret


def get_base_envvars():
    """Return base envvars of django project"""
    common_envvar_names = {
        "BASE_DIR",
        "BASE_PATH",
        "ROOT_URLCONF",
    }

    # Envvar names extracted from: from django.conf import global_settings
    #
    # Use this module on this function causes an unexpected behavior on tests
    #
    django_base_envvar_names = {
        "ABSOLUTE_URL_OVERRIDES",
        "ADMINS",
        "ALLOWED_HOSTS",
        "APPEND_SLASH",
        "AUTHENTICATION_BACKENDS",
        "AUTH_PASSWORD_VALIDATORS",
        "AUTH_USER_MODEL",
        "BASE_DIR",
        "BASE_PATH",
        "CACHES",
        "CACHE_MIDDLEWARE_ALIAS",
        "CACHE_MIDDLEWARE_KEY_PREFIX",
        "CACHE_MIDDLEWARE_SECONDS",
        "CSRF_COOKIE_AGE",
        "CSRF_COOKIE_DOMAIN",
        "CSRF_COOKIE_HTTPONLY",
        "CSRF_COOKIE_NAME",
        "CSRF_COOKIE_PATH",
        "CSRF_COOKIE_SAMESITE",
        "CSRF_COOKIE_SECURE",
        "CSRF_FAILURE_VIEW",
        "CSRF_HEADER_NAME",
        "CSRF_TRUSTED_ORIGINS",
        "CSRF_USE_SESSIONS",
        "DATABASES",
        "DATABASE_ROUTERS",
        "DATA_UPLOAD_MAX_MEMORY_SIZE",
        "DATA_UPLOAD_MAX_NUMBER_FIELDS",
        "DATETIME_FORMAT",
        "DATETIME_INPUT_FORMATS",
        "DATE_FORMAT",
        "DATE_INPUT_FORMATS",
        "DEBUG",
        "DEBUG_PROPAGATE_EXCEPTIONS",
        "DECIMAL_SEPARATOR",
        "DEFAULT_CHARSET",
        "DEFAULT_CONTENT_TYPE",
        "DEFAULT_EXCEPTION_REPORTER_FILTER",
        "DEFAULT_FILE_STORAGE",
        "DEFAULT_FROM_EMAIL",
        "DEFAULT_INDEX_TABLESPACE",
        "DEFAULT_TABLESPACE",
        "DISALLOWED_USER_AGENTS",
        "EMAIL_BACKEND",
        "EMAIL_HOST",
        "EMAIL_HOST_PASSWORD",
        "EMAIL_HOST_USER",
        "EMAIL_PORT",
        "EMAIL_SSL_CERTFILE",
        "EMAIL_SSL_KEYFILE",
        "EMAIL_SUBJECT_PREFIX",
        "EMAIL_TIMEOUT",
        "EMAIL_USE_LOCALTIME",
        "EMAIL_USE_SSL",
        "EMAIL_USE_TLS",
        "FILE_CHARSET",
        "FILE_UPLOAD_DIRECTORY_PERMISSIONS",
        "FILE_UPLOAD_HANDLERS",
        "FILE_UPLOAD_MAX_MEMORY_SIZE",
        "FILE_UPLOAD_PERMISSIONS",
        "FILE_UPLOAD_TEMP_DIR",
        "FIRST_DAY_OF_WEEK",
        "FIXTURE_DIRS",
        "FORCE_SCRIPT_NAME",
        "FORMAT_MODULE_PATH",
        "FORM_RENDERER",
        "IGNORABLE_404_URLS",
        "INSTALLED_APPS",
        "INTERNAL_IPS",
        "LANGUAGES",
        "LANGUAGES_BIDI",
        "LANGUAGE_CODE",
        "LANGUAGE_COOKIE_AGE",
        "LANGUAGE_COOKIE_DOMAIN",
        "LANGUAGE_COOKIE_NAME",
        "LANGUAGE_COOKIE_PATH",
        "LOCALE_PATHS",
        "LOGGING",
        "LOGGING_CONFIG",
        "LOGIN_REDIRECT_URL",
        "LOGIN_URL",
        "LOGOUT_REDIRECT_URL",
        "MANAGERS",
        "MEDIA_ROOT",
        "MEDIA_URL",
        "MESSAGE_STORAGE",
        "MIDDLEWARE",
        "MIGRATION_MODULES",
        "MONTH_DAY_FORMAT",
        "NUMBER_GROUPING",
        "PASSWORD_HASHERS",
        "PASSWORD_RESET_TIMEOUT_DAYS",
        "PREPEND_WWW",
        "ROOT_URLCONF",
        "SECRET_KEY",
        "SECURE_BROWSER_XSS_FILTER",
        "SECURE_CONTENT_TYPE_NOSNIFF",
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        "SECURE_HSTS_PRELOAD",
        "SECURE_HSTS_SECONDS",
        "SECURE_PROXY_SSL_HEADER",
        "SECURE_REDIRECT_EXEMPT",
        "SECURE_SSL_HOST",
        "SECURE_SSL_REDIRECT",
        "SERVER_EMAIL",
        "SESSION_CACHE_ALIAS",
        "SESSION_COOKIE_AGE",
        "SESSION_COOKIE_DOMAIN",
        "SESSION_COOKIE_HTTPONLY",
        "SESSION_COOKIE_NAME",
        "SESSION_COOKIE_PATH",
        "SESSION_COOKIE_SAMESITE",
        "SESSION_COOKIE_SECURE",
        "SESSION_ENGINE",
        "SESSION_EXPIRE_AT_BROWSER_CLOSE",
        "SESSION_FILE_PATH",
        "SESSION_SAVE_EVERY_REQUEST",
        "SESSION_SERIALIZER",
        "SHORT_DATETIME_FORMAT",
        "SHORT_DATE_FORMAT",
        "SIGNING_BACKEND",
        "SILENCED_SYSTEM_CHECKS",
        "STATICFILES_DIRS",
        "STATICFILES_FINDERS",
        "STATICFILES_STORAGE",
        "STATIC_ROOT",
        "STATIC_URL",
        "TEMPLATES",
        "TEST_NON_SERIALIZED_APPS",
        "TEST_RUNNER",
        "THOUSAND_SEPARATOR",
        "TIME_FORMAT",
        "TIME_INPUT_FORMATS",
        "TIME_ZONE",
        "USE_I18N",
        "USE_L10N",
        "USE_THOUSAND_SEPARATOR",
        "USE_TZ",
        "USE_X_FORWARDED_HOST",
        "USE_X_FORWARDED_PORT",
        "WSGI_APPLICATION",
        "X_FRAME_OPTIONS",
        "YEAR_MONTH_FORMAT",
    }

    return common_envvar_names.union(django_base_envvar_names)
