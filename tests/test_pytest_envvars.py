from collections import Counter
from pytest_envvars import set_randomized_env_vars_from_list


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

    result = django_testdir.runpytest()
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

    result = django_testdir.runpytest()
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

    result = django_testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_context_values PASSED*",
        "*test_some_function PASSED*",
    ])


def test_set_randomized_env_vars_from_list():
    # given:
    input_env_vars = [
        'FOO=123',
        'BAR=1==2',
        'BAZ=====1==2',
    ]
    expected_env_vars = [
        ('FOO', '123'),
        ('BAR', '1==2'),
        ('BAZ', '====1==2'),
    ]
    ignored_django_envvars = set()
    ignored_envvars = set()

    # when
    result = set_randomized_env_vars_from_list(
        input_env_vars, ignored_django_envvars, ignored_envvars
    )

    # then:
    assert result == expected_env_vars
