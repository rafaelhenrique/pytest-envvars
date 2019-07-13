==============
pytest-envvars
==============

.. image:: https://travis-ci.org/rafaelhenrique/pytest-envvars.svg?branch=master
    :target: https://travis-ci.org/rafaelhenrique/pytest-envvars
    :alt: See Build Status on Travis CI

Pytest plugin to validate use of envvars on your tests


Note
----

Warning: pytest-envvars is **beta**.

What is pytest-envvars?
-----------------------

pytest-envvars change values of environment variables on your unit tests to check consistency of mocks. If the test has a wrong mock, this test will be broken.

pytest-envvars changes the values of the environment variables in your unit tests to check the consistency of the mocks. If the test has a wrong mock, this test will be broken due to changes in the original values of the environment variables.

Install
-------

.. code-block:: bash

    $ pip install pytest-envvars

Use
---

.. code-block:: bash

    $ pytest --envvars-validate
