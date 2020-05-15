Changelog
---------

1.1.0
~~~~~
* Add command line parameter called '--validate-envvars' to enable execution of plugin.
* Fix plugin path on to run tox lint

1.0.0
~~~~~

* First stable release \o/
* Remove parameter '--envvars-validate';
* Now all configuration of pytest-envvars will be on 'pytest.ini' by 'pytestenvvars__env_files' and 'pytestenvvars__dont_randomize_envvars' configurations.

0.0.1
~~~~~

* First version \o/
* Validate wrong mocks for 'global variables' with a envvar value;
* Change values of envvars with *random.choices* using '1' or '0';
* Some features to use this plugin with Django.
