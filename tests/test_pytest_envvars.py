from pytest_envvars.django_utils import get_custom_envvars, is_django_project
from pytest_envvars.utils import get_modules_to_reload


def test_read_envvar_from_context_with_incorrect_test(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        @pytest.mark.parametrize('context_variable, content', [
            ('pytest_envvar_str', 'Rafael'),
            ('global_variable', 'Rafael_global'),
        ], ids=[
            'pytest_envvar_str',
            'global_variable',
        ])
        def test_context_values(context_variable, content, client):
            response = client.get('/')
            assert response.context[context_variable] == content

    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 1
    result.stdout.fnmatch_lines([
        "*test_context_values*pytest_envvar_str* FAILED*",
        "*test_context_values*global_variable* FAILED*",
    ])


def test_read_envvar_from_context_with_correct_test(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        @pytest.mark.parametrize('context_variable, content', [
            ('pytest_envvar_str', 'Rafael'),
            ('global_variable', 'Rafael_global'),
        ], ids=[
            'pytest_envvar_str',
            'global_variable',
        ])
        def test_context_values(context_variable, content, client, settings):
            settings.PYTEST_ENVVAR_STR = 'Rafael'
            response = client.get('/')
            assert response.context[context_variable] == content
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*test_context_values*pytest_envvar_str* PASSED*",
        "*test_context_values*global_variable* PASSED*",
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
