from pytest_envvars.lazy_django import is_django_project


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


def test_is_django_project_with_django_project(monkeypatch):
    DJANGO_SETTINGS_MODULE = "tests.pytest_envvars_django_test.pytest_envvars_django_test.settings"
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    assert is_django_project() is True
