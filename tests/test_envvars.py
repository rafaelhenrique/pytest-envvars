def test_simple_model_test(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        from tests.pytest_envvars_django_test.core.models import Product

        pytestmark = pytest.mark.django_db

        def test_product_exists_with_products():
            Product.objects.create(name='Mouse')
            assert Product.objects.exists() is True
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*test_product_exists_with_products PASSED*"])


def test_simple_get_request(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        def test_get_home_page(client):
            response = client.get('/')
            assert response.status_code == 200
            assert 'Only for test purpouses' in str(response.content)
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*test_get_home_page PASSED*"])


def test_read_envvar_from_context_without_set_environment(django_testdir):
    django_testdir.create_test_module("""
        import pytest

        pytestmark = pytest.mark.django_db

        def test_context_values(client):
            response = client.get('/')
            assert response.context['pytest_envvar_str'] == 'Rafael'
    """)

    result = django_testdir.runpytest('--envvars-validate')
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*test_context_values PASSED*"])
