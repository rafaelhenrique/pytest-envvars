from pytest_envvars.utils import get_modules_to_reload


def test_get_modules_to_reload():
    from pytest_envvars_modules_test import main
    from pytest_envvars_modules_test.generic import generic

    modules = get_modules_to_reload(main.__file__)
    assert modules == {'drink', 'listen', 'drink.beer'}

    modules = get_modules_to_reload(generic.__file__)
    assert modules == {'drink', 'listen', 'drink.beer'}
