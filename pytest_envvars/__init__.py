import glob
import os
import random

import pytest


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
    fullpath_filenames = []
    for filename in early_config.getini("env_files"):
        fullpath_filenames += glob.glob(f'**/{filename}', recursive=True)

    for filename in fullpath_filenames:
        with open(filename, 'r', encoding='utf-8-sig') as config_file:
            for line in config_file:
                envvar, *_ = line.partition('=')
                envvar = envvar.strip()

            os.environ[envvar] = random.choice(['0', '1'])
