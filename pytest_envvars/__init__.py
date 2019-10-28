import os
import random
from pathlib import Path

import pytest
from pytest_envvars.django_utils import is_django_project, get_base_envvars


def pytest_addoption(parser):
    """Parse pytest.ini env_files section"""
    parser.addini(
        'pytestenvvars__env_files',
        type='linelist',
        help='A line separated list of env files to parse',
    )
    parser.addini(
        'pytestenvvars__dont_randomize_envvars',
        type='linelist',
        help='A line separated list of envvars not to be randomized',
    )


def set_randomized_env_vars_from_list(
    source_list, ignored_django_envvars, ignored_envvars
):
    """
    param `source_list` is a list of strings like: 'FOO=barbaz'
    here the value is randomized like: FOO=1010101,
    and set the new value in os.environ['FOO'] = 1010101
    """

    randomized_envvars = []
    for line in source_list:
        envvar, _, value = line.partition('=')
        envvar = envvar.strip()
        value = value.strip()
        randomized_envvars.append((envvar, value))

        if envvar in ignored_django_envvars or envvar in ignored_envvars:
            os.environ[envvar] = value
        else:
            os.environ[envvar] = random.choice(['0', '1'])

    return randomized_envvars


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    """Load config files and randomize envvars from pytest.ini"""
    ignored_django_envvars = get_base_envvars() if is_django_project() else set()
    ignored_envvars = early_config.getini("pytestenvvars__dont_randomize_envvars")
    fullpath_filenames = set()
    for filename in early_config.getini("pytestenvvars__env_files"):
        fullpath_filenames.update({
            p.absolute() for p in Path().rglob(filename)
            if p.is_file()
        })

    for filename in fullpath_filenames:
        with open(filename, 'r', encoding='utf-8-sig') as config_file:
            set_randomized_env_vars_from_list(
                config_file.readlines(),
                ignored_django_envvars,
                ignored_envvars
            )

    # very useful in unit tests...
    # os.environ['PYTEST_ENVVARS_DEBUG'] = f"{envvars} - {ignored_envvars}"
