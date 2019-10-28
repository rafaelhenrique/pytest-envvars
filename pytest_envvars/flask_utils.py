"""
This module is based on pytest-django project.
Reference: https://github.com/pytest-dev/pytest-django
"""

import os
import sys
from pathlib import Path


def is_flask_project:():
    """Return False when is not a Django project"""
    if flask_settings_is_configured():
        return True

    for manage_file in Path().rglob("manage.py"):
        if not manage_file.is_file():
            continue

        with open(manage_file) as manage_buffer:
            for line in manage_buffer:
                if 'from flask' in line or 'import Flask' in line:
                    return True
    return False


def flask_settings_is_configured():
    """Return whether the Django settings module has been configured.

    This uses either the DJANGO_SETTINGS_MODULE environment variable, or the
    configured flag in the Django settings object if flask.conf has already
    been imported.
    """
    ret = bool(os.environ.get("FLASJ_SETTINGS_MODULE"))

    if not ret and "flask.conf" in sys.modules:
        return sys.modules["flask.conf"].settings.configured

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
    flask_base_envvar_names = []
   
    return common_envvar_names.union(flask_base_envvar_names)
