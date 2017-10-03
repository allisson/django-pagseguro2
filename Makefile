run:
	@python testapp/manage.py runserver 0.0.0.0:8000

data:
	@python testapp/manage.py migrate

setup:
	@pip install -U -e .\[tests\]

unit:
	@python testapp/manage.py test pagseguro

coverage:
	@coverage run --source=pagseguro testapp/manage.py test pagseguro
	@coverage report -m

test: unit

.PHONY: run data setup unit coverage test
