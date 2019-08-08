import pytest
from pytest_envvars.django_utils import get_custom_envvars, is_django_project


def test_is_django_project_without_django_project():
    assert is_django_project() is False


def test_is_django_project_with_django_project(default_django_environment):
    assert is_django_project() is True


@pytest.mark.skip("This function needs an fix, we cannot call settings._explicit_settings")
def test_get_custom_envvars(default_django_environment):
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
