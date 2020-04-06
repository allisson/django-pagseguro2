clean: clean-eggs clean-build
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

lint:
	flake8 --ignore=E501,W503 pagseguro/*.py testapp/*.py
	isort --check-only **/*.py
	black --check --quiet pagseguro/*.py testapp/*.py

test:
	testapp/manage.py test pagseguro

build: test
	python setup.py sdist
	python setup.py bdist_wheel

release: build
	twine upload dist/*
