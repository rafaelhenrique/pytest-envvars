from collections import Counter

from pytest_envvars.django_utils import get_custom_envvars, is_django_project
from pytest_envvars.utils import get_modules_to_reload


def test_read_envvar_from_context_with_wrong_tests(django_testdir):
    django_testdir.create_test_module("""
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function():
            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 1
    result.stdout.fnmatch_lines([
        "*test_context_values FAILED*",
        "*test_some_function FAILED*",
    ])
    output = result.stdout.str().split()
    assert Counter(output)['AssertionError:'] == 2


def test_read_envvar_from_context_with_correct_test(django_testdir):
    django_testdir.create_test_module("""
        import pytest
        from tests.pytest_envvars_django_test.core.views import some_function

        pytestmark = pytest.mark.django_db

        @pytest.mark.skip(reason="TODO: Has a bug here! This test needs pass!")
        def test_context_values(client, monkeypatch):
            from tests.pytest_envvars_django_test.core import views
            monkeypatch.setattr(views, 'GLOBAL_VARIABLE', 'xablau')

            response = client.get('/')
            assert response.context['pytest_envvar_generic_use'] == 'xablau'

        def test_some_function(monkeypatch):
            from tests.pytest_envvars_django_test.core import views
            monkeypatch.setattr(views, 'GLOBAL_VARIABLE', 'xablau')

            assert some_function() == 'xablau'
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_some_function PASSED*",
    ])


def test_is_django_project_without_django_project():
    assert is_django_project() is False


def test_is_django_project_with_django_project(django_environment):
    assert is_django_project() is True


def test_get_custom_envvars(django_environment):
    custom_envvars = get_custom_envvars()
    assert custom_envvars == {
        "PYTEST_ENVVAR_FLOAT",
        "PYTEST_ENVVAR_INT",
        "PYTEST_ENVVAR_LIST",
        "PYTEST_ENVVAR_TUPLE",
        "PYTEST_ENVVAR_STR",
        "PYTEST_ENVVAR_BOOL",
        "PYTEST_ENVVAR_GENERIC_USE",
    }


def test_get_modules_to_reload():
    from pytest_envvars_modules_test import main
    from pytest_envvars_modules_test.generic import generic

    modules = get_modules_to_reload(main.__file__)
    assert modules == {'drink', 'listen', 'drink.beer'}

    modules = get_modules_to_reload(generic.__file__)
    assert modules == {'drink', 'listen', 'drink.beer'}
