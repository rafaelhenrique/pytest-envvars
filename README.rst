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
