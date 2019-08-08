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


def get_base_envvars():
    """Return base envvars of django project"""
    from django.conf import global_settings
    common_envvar_names = {
        "BASE_DIR",
        "BASE_PATH",
        "ROOT_URLCONF",
    }
    django_global_settings = set(global_settings.__dict__.keys()).union(common_envvar_names)
    django_global_settings = {
        conf for conf in django_global_settings
        if not conf.startswith('_') and not conf.islower()
    }

    return django_global_settings
