import pathlib
import shutil
from textwrap import dedent

import pytest

pytest_plugins = "pytester"

REPOSITORY_ROOT = pathlib.Path(__file__).parent
PROJECT_NAME = "pytest_envvars_django_test"
DJANGO_SETTINGS_MODULE = "tests.pytest_envvars_django_test.pytest_envvars_django_test.settings"


@pytest.fixture(scope="function")
def django_testdir(request, testdir, monkeypatch):
    project_root = testdir.tmpdir
    project_source = REPOSITORY_ROOT.joinpath(PROJECT_NAME)
    project_destination = project_root.join(PROJECT_NAME)

    shutil.copytree(project_source, project_destination)
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    monkeypatch.setenv("SECRET_KEY", "xablau")

    def create_test_module(test_code, filename="test_the_test.py"):
        testfile = project_destination.join(filename)
        testfile.write(dedent(test_code), ensure=True)
        return testfile

    testdir.create_test_module = create_test_module
    testdir.project_root = project_root

    testdir.makeini(
        """
        [pytest]
        addopts = -vv --tb=native
        """
    )
    return testdir
