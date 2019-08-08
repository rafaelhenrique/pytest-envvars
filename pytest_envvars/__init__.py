from pytest_envvars.validators import PytestEnvvarsValidator, RandomizeEnvvars
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
    group.addoption(
        '--randomize-envvars',
        action='store_true',
        dest='randomize_envvars',
        default=False,
        help='Insert a random values on envvars of your tests'
    )


def pytest_cmdline_main(config):
    """Get parameters from command line and make actions"""
    if config.option.envvars_validate and is_django_project():
        pytest_envvars_validator = PytestEnvvarsValidator()
        config.pluginmanager.register(pytest_envvars_validator)
    elif config.option.randomize_envvars and is_django_project():
        randomize_envvars = RandomizeEnvvars()
        config.pluginmanager.register(randomize_envvars)
