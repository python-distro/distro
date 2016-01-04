.PHONY: release install files test docs prepare publish

all:
	@echo "make release - prepares a release and publishes it"
	@echo "make dev - prepares a development environment (includes tests)"
	@echo "make instdev - prepares a development environment (no tests)"
	@echo "make install - install on local system"
	@echo "make test - run tox"
	@echo "make publish - upload to pypi"

release: publish

dev: instdev test

instdev:
	pip install -r dev-requirements.txt
	python setup.py develop

install:
	python setup.py install

test:
	sudo pip install 'tox>=1.7.2'
	tox

publish:
	python setup.py sdist upload

