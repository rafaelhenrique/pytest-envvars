import random
import os


class PytestEnvvarsValidator:

    def pytest_runtest_setup(self, item):
        os.environ['PYTEST_ENVVAR_STR'] = random.choice(['0', '1'])
