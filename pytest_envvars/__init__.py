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

    envvars = []
    for filename in fullpath_filenames:
        with open(filename, 'r', encoding='utf-8-sig') as config_file:
            for line in config_file:
                envvar, _, value = line.partition('=')
                envvar = envvar.strip()
                value = value.strip()
                envvars.append((envvar, value))

                if envvar in ignored_django_envvars or envvar in ignored_envvars:
                    os.environ[envvar] = value
                else:
                    os.environ[envvar] = random.choice(['0', '1'])

    # very useful in unit tests...
    # os.environ['PYTEST_ENVVARS_DEBUG'] = f"{envvars} - {ignored_envvars}"
