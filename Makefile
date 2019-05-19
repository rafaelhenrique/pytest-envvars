.PHONY: help
help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: clean-eggs clean-build ## Clean all thrash files (cached, builds .. etc)
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

install-tox:
	@pip install tox

test: install-tox ## Run tests with Python 3.7
	tox -e py37

install-tools-for-release:
	@pip install --upgrade setuptools wheel twine

dist: ## Create a dist directory
	@python setup.py sdist bdist_wheel

test-release: clear install-tools-for-release dist ## Release package to Test PyPI
	@python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: clear install-tools-for-release dist ## Release package to PyPI
	@python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

