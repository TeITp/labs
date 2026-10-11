.PHONY: install test unit fail-fast collect clean

install:
	poetry install

test:
	poetry run pytest -v

unit:
	poetry run pytest -m unit -v

fail-fast:
	poetry run pytest -x --tb=short

collect:
	poetry run pytest --collect-only -q

clean:
	rm -rf .pytest_cache __pycache__
