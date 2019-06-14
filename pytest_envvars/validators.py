import random
import os

from importlib import reload


class PytestEnvvarsValidator:

    def pytest_runtest_setup(self, item):
        os.environ['PYTEST_ENVVAR_STR'] = random.choice(['0', '1'])

        from django import conf
        from pytest_envvars_django_test import settings

        reload(conf)
        reload(settings)
