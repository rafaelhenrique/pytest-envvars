==============
pytest-envvars
==============

.. image:: https://travis-ci.org/rafaelhenrique/pytest-envvars.svg?branch=master
    :target: https://travis-ci.org/rafaelhenrique/pytest-envvars
    :alt: See Build Status on Travis CI

Pytest plugin to validate use of envvars on your tests

What is pytest-envvars?
-----------------------

pytest-envvars randomize values of environment variables on your unit tests to check consistency of mocks about configuration. If the test has a wrong mock, this test will be broken.

Install
-------

.. code-block:: bash

    $ pip install pytest-envvars

Use
---

You need write some changes on ``pytest.ini`` file, like that...

.. code-block:: bash

    [pytest]
    pytestenvvars__env_files =
        .env
    pytestenvvars__dont_randomize_envvars =
        CACHE_URL

On this example above the plugin read ``.env`` file (from ``pytestenvvars__env_files`` section) of your project and randomize **ALL** envvar configuration on that file, if you dont need randomize some envvar configuration you need add this envvar to ``pytestenvvars__dont_randomize_envvars`` section like shown above.

Before that configuration to run validation you need run pytest with flag ``--validate-envvars``, like that...

.. code-block:: bash

    pytest --validate-envvars

To debug purpose you can use ``--envvars-value`` to set a default value for all envvars. This parameter accept only two options 0 or 1, see this example:

.. code-block:: bash

    pytest --validate-envvars --envvars-value=0

Using the plugin that way you will apply the value 0 to ALL of your envvars.
