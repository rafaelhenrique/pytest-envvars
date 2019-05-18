install-tox:
	@pip install tox

test: install-tox
	tox -e py37

