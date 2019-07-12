import random
import os
from importlib import reload, import_module

from .django_utils import get_custom_envvars, is_django_project
from .utils import get_modules_to_reload


class PytestEnvvarsValidator:

    def pytest_runtest_setup(self, item):
        for envvar in get_custom_envvars():
            os.environ[envvar] = random.choice(['0', '1'])

        test_filename = item.module.__file__
        modules = get_modules_to_reload(test_filename)

        # dont reload mocks
        dont_reload_modules = ['pdb', 'unittest.mock']
        mocks = getattr(item.function, 'patchings', [])
        for mock in mocks:
            mocked_object = mock.getter()
            module = getattr(mocked_object, '__module__', None) or getattr(mocked_object, '__name__', None)
            dont_reload_modules.append(module)

        if is_django_project:
            from django import conf
            settings_str = os.environ.get("DJANGO_SETTINGS_MODULE")
            settings = import_module(settings_str)
            reload(conf)
            reload(settings)

        for module in dont_reload_modules:
            try:
                modules.remove(module)
            except KeyError:
                pass

        for module_str in modules:
            module = import_module(module_str)
            reload(module)
