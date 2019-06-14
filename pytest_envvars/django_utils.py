"""
This module is based on pytest-django project.
Reference: https://github.com/pytest-dev/pytest-django
"""

import os
import sys


def is_django_project():
    """Return False when no Django settings are available"""
    if django_settings_is_configured():
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
