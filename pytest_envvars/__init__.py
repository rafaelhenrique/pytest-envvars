import os
import random
from pathlib import Path

import pytest
from pytest_envvars.django_utils import is_django_project, get_base_envvars


def pytest_addoption(parser):
    """Parse pytest.ini env_files section"""
    parser.addini(
        'env_files',
        type='linelist',
        help='A line separated list of env files to parse',
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    """Load config files and randomize envvars from pytest.ini"""
    ignored_django_envvars = get_base_envvars() if is_django_project() else set()
    fullpath_filenames = set()
    for filename in early_config.getini("env_files"):
        fullpath_filenames.update({
            p.absolute() for p in Path().rglob(filename)
            if p.is_file()
        })

    for filename in fullpath_filenames:
        with open(filename, 'r', encoding='utf-8-sig') as config_file:
            for line in config_file:
                envvar, *_ = line.partition('=')
                envvar = envvar.strip()

                if envvar in ignored_django_envvars:
                    continue

                os.environ[envvar] = random.choice(['0', '1'])
