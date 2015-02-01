.PHONY: flake8 test coverage

flake8:
	flake8 --ignore=W999 payer_api

test:
	python payer_api/tests/runtests.py

coverage:
	coverage erase
	PYTHONPATH=. coverage run --branch ./payer_api/tests/runtests.py
	coverage combine
	coverage html
	coverage report
