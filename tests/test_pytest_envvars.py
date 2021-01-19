from collections import Counter
from pathlib import PosixPath
from unittest import mock

from pytest_envvars import (get_fullpath_filenames,
                            set_randomized_env_vars_from_file)


def test_read_envvar_from_context_with_wrong_tests(
    django_testdir,
    default_env_file,
    default_tox_ini_file,
    default_django_environment
):
    django_testdir.create_test_module("""
        import os
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function(settings):
            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest("--validate-envvars")
    assert result.ret == 1
    result.stdout.fnmatch_lines([
        "*test_context_values FAILED*",
        "*test_some_function FAILED*",
    ])
    output = result.stdout.str().split()
    assert Counter(output)['AssertionError:'] == 2


def test_read_envvar_from_context_with_correct_test(
    django_testdir,
    default_env_file,
    default_tox_ini_file,
    default_django_environment,
):
    django_testdir.create_test_module("""
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        def test_context_values(client, settings):
            settings.PYTEST_ENVVAR_GENERIC_USE = 'xablau'

            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function(monkeypatch):
            from tests.pytest_envvars_django_test.core import views
            monkeypatch.setattr(views, 'GLOBAL_VARIABLE', 'xablau')

            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest("--validate-envvars")
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_context_values PASSED*",
        "*test_some_function PASSED*",
    ])


def test_read_envvar_from_context_with_wrong_tests_and_ignored_envvars(
    django_testdir,
    default_env_file,
    default_django_environment
):
    django_testdir.makeini(
        """
        [pytest]
        addopts = -vv --tb=native
        pytestenvvars__env_files =
            .env
        pytestenvvars__dont_randomize_envvars =
            PYTEST_ENVVAR_GENERIC_USE
        """
    )
    django_testdir.create_test_module("""
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function(settings):
            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest("--validate-envvars")
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_context_values PASSED*",
        "*test_some_function PASSED*",
    ])


def test_read_envvar_from_context_with_wrong_tests_without_validate_envvars_param(
    django_testdir,
    default_env_file,
    default_tox_ini_file,
    default_django_environment
):
    django_testdir.create_test_module("""
        import os
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function(settings):
            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_context_values PASSED*",
        "*test_some_function PASSED*",
    ])


def test_set_randomized_env_vars_from_file(tmp_path):
    # given:
    input_env_vars = [
        'FOO=123',
        'BAR=1==2',
        'BAZ=====1==2',
    ]
    expected_env_vars = {
        'FOO': '123',
        'BAR': '1==2',
        'BAZ': '====1==2',
    }
    ignored_django_envvars = set()
    ignored_envvars = set()
    dotenv_file = tmp_path / ".env"
    dotenv_file.write_text('\n'.join(input_env_vars))

    # when
    result = set_randomized_env_vars_from_file(
        dotenv_file, ignored_django_envvars, ignored_envvars
    )

    # then:
    assert result == expected_env_vars


def test_get_value_of_envvar_by_param(
    django_testdir,
    default_env_file,
    default_tox_ini_file,
    default_django_environment,
):
    django_testdir.create_test_module("""
        import pytest

        def test_get_value_of_envvar_by_param(settings):
            assert settings.PYTEST_ENVVAR_GENERIC_USE == '0'

    """)

    result = django_testdir.runpytest("--validate-envvars", "--envvars-value=0")
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_get_value_of_envvar_by_param PASSED*",
    ])


def test_get_value_of_envvar_by_param_with_wrong_value(
    django_testdir,
    default_env_file,
    default_tox_ini_file,
    default_django_environment,
):
    django_testdir.create_test_module("""
        import pytest

        def test_get_value_of_envvar_by_param_with_wrong_value(settings):
            assert settings.PYTEST_ENVVAR_GENERIC_USE == '0'

    """)

    result = django_testdir.runpytest("--validate-envvars", "--envvars-value=1")
    assert result.ret == 1
    result.stdout.fnmatch_lines([
        "*test_get_value_of_envvar_by_param_with_wrong_value FAILED*",
    ])


@mock.patch("pytest_envvars.Path.rglob")
def test_get_fullpath_filenames(
    mocked_rglob,
    default_env_file,
):
    class FakePosixPath:
        def __init__(self, *args, **kwargs):
            pass

        def is_file(self):
            return True

        def absolute(self):
            return PosixPath("fakedir/.env")

    mocked_rglob.return_value = [FakePosixPath("pytest_envvars_django_test/.env")]
    fullpath_env_files = get_fullpath_filenames([".env"])

    assert fullpath_env_files == {PosixPath("fakedir/.env")}


@mock.patch('pytest_envvars.Path.rglob')
def test_get_fullpath_filenames_without_file(
    mocked_rglob,
    default_env_file,
):
    fullpath_env_files = get_fullpath_filenames([".xablau"])
    assert fullpath_env_files == set()
