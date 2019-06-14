import random
import os

from .django_utils import get_custom_envvars


class PytestEnvvarsValidator:

    def pytest_runtest_setup(self, item):
        for envvar in get_custom_envvars():
            os.environ[envvar] = random.choice(['0', '1'])
