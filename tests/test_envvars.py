def test_read_envvar_from_context_without_set_environment(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_str'] == 'Rafael'
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 1
    result.stdout.fnmatch_lines(["*test_context_values FAILED*"])


def test_read_envvar_from_context_setting_correct_environment(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        def test_context_values(client, settings):
            settings.PYTEST_ENVVAR_STR = 'Rafael'
            response = client.get('/')
            assert response.context['pytest_envvar_str'] == 'Rafael'
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*test_context_values PASSED*"])
