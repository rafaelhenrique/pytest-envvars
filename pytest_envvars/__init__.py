import os
import random
from pathlib import Path, PosixPath
from typing import Any, List, Set

import pytest

from pytest_envvars.django_utils import get_base_envvars, is_django_project


def pytest_addoption(parser):
    """Parse pytest.ini env_files section"""
    group = parser.getgroup("envvars")
    group.addoption(
        "--validate-envvars",
        action="store_true",
        dest="validate_envvars",
        default=False,
        help="Validate envvars mocks",
    )
    group.addoption(
        "--envvars-value",
        dest="envvars_value",
        default=False,
        type=int,
        choices=[0, 1],
        help="Select value of envvars",
    )
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
    envvar_value_list: List[str],
    ignored_django_envvars: Set[str],
    ignored_envvars: Set[str],
    randomize: bool = False,
    envvars_value: Any = None,
) -> List[tuple]:
    """Get envvar_value_list split this list into envvar and value and randomize values.

    Params:
        envvar_value_list (list): list with envvars and values, eg. ['FOO=123', 'BAR=432']
        ignored_django_envvars (set): set with envvars of django (used only in django projects)
        ignored_envvars (set): set with ignored envvars added in configuration file
        randomize (bool): True for randomize OR False for no randomize envvars
        envvars_value (Any or None): Pass some value for all envvars OR None if dont pass anything

    Returns:
        List(tuples): List with tuples envvar and value, eg. [('FOO', '0'), ('BAR', '0')]
    """
    randomized_envvars = []
    for line in envvar_value_list:
        if line.startswith("#") or line.strip() == "":
            continue

        envvar, _, value = line.partition('=')
        envvar = envvar.strip()
        value = value.strip()
        randomized_envvars.append((envvar, value))

        no_randomize = any([
            randomize is False,
            envvar in ignored_django_envvars,
            envvar in ignored_envvars,
        ])

        if no_randomize:
            os.environ[envvar] = value
        else:
            os.environ[envvar] = envvars_value if envvars_value else random.choice(['0', '1'])

    return randomized_envvars


def get_fullpath_filenames(filenames: List[str]) -> Set[PosixPath]:
    """Get filenames list and return a fullpath of these files

    Params:
        filenames (list): List of strings with filenames

    Returns:
        Set[PosixPath]: A set with one or more PosixPath objects
    """
    fullpath_filenames = set()
    for filename in filenames:
        fullpath_filenames.update({
            path.absolute() for path in Path().rglob(filename)
            if path.is_file()
        })
    return fullpath_filenames


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    """Load config files and randomize envvars from pytest.ini"""

    parsed_args = parser.parse(args)

    envvars_value = None
    if parsed_args.envvars_value is not False:
        envvars_value = str(parsed_args.envvars_value)

    ignored_django_envvars = get_base_envvars() if is_django_project() else set()
    ignored_envvars = early_config.getini("pytestenvvars__dont_randomize_envvars")
    env_files = early_config.getini("pytestenvvars__env_files")
    fullpath_env_files = get_fullpath_filenames(env_files)
    for filename in fullpath_env_files:
        with open(filename, 'r', encoding='utf-8-sig') as config_file:
            set_randomized_env_vars_from_list(
                config_file.readlines(),
                ignored_django_envvars,
                ignored_envvars,
                parsed_args.validate_envvars,
                envvars_value,
            )

    # very useful in unit tests...
    # os.environ['PYTEST_ENVVARS_DEBUG'] = f"{envvars} - {ignored_envvars}"
