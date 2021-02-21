.DEFAULT_GOAL := help
.PHONY: changelog coverage deps help lint push test

coverage:  ## Run tests with coverage
	coverage erase
	coverage run --include=face_group/* -m pytest -ra
	coverage report -m

deps:  ## Install dependencies
	poetry install

lint:  ## Lint and static-check
	poetry run black face_group
	poetry run isort face_group
	poetry run flake8 face_group
	poetry run pylint face_group
	poetry run mypy face_group

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	pytest -ra