.PHONY: install test before cov html gate clean

install:
	poetry install

test:
	poetry run pytest -v

before:
	poetry run pytest test_app.py -k трикутник --cov=app --cov-report=term-missing

cov:
	poetry run coverage erase
	poetry run coverage run -m pytest
	poetry run coverage report -m

html: cov
	poetry run coverage html

gate:
	poetry run pytest --cov=app --cov-fail-under=90

clean:
	rm -rf .pytest_cache __pycache__ .coverage htmlcov
