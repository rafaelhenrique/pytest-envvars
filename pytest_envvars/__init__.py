from pytest_envvars.validators import PytestEnvvarsValidator
from pytest_envvars.django_utils import is_django_project


def pytest_addoption(parser):
    """Parse parameters from command line"""
    group = parser.getgroup('envvars')
    group.addoption(
        '--envvars-validate',
        action='store_true',
        dest='envvars_validate',
        default=False,
        help='Validate envvars of your tests'
    )


def pytest_cmdline_main(config):
    """Get parameters from command line and make actions"""
    if config.option.envvars_validate and is_django_project():
        pytest_envvars_validator = PytestEnvvarsValidator()
        config.pluginmanager.register(pytest_envvars_validator)
