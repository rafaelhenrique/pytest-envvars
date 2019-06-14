import random
import os

from importlib import reload


def pytest_addoption(parser):
    """Parse parameters from command line"""
    group = parser.getgroup('envvars')
    group.addoption(
        '--envvars-validate',
        action='store_true',
        dest='envvars_validate',
        default=False,
        help='Validate envvars of your tests'
    )


def pytest_cmdline_main(config):
    """Get parameters from command line and make actions"""
    if config.option.envvars_validate:
        pytest_envvars_validator = PytestEnvvarsValidator()
        config.pluginmanager.register(pytest_envvars_validator)


class PytestEnvvarsValidator:

    def pytest_runtest_setup(self, item):
        os.environ['PYTEST_ENVVAR_STR'] = random.choice(['0', '1'])

        from django import conf
        from pytest_envvars_django_test import settings
        reload(conf)
        reload(settings)
