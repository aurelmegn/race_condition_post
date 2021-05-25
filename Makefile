
SHELL := /bin/bash
TEST_SUITE=-m "not full"
.PHONY: all clean test install run deploy down migrate migration install_poetry install_prod

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

all: clean test install run deploy

test:
	mkdir -p coverage/html/
	poetry run pytest tests -vvv --show-capture=all --cov=app --cov-report html:coverage/html/

test_full: TEST_SUITE=
test_full: test

install_poetry:
	pip install --upgrade pip
	pip install poetry


install:
	@$(MAKE) generate_dot_env
	@$(MAKE) install_poetry
	poetry install
	@$(MAKE) migrate

install_prod:
	@$(MAKE) generate_dot_env
	@$(MAKE) install_poetry
	poetry install --no-dev
	@$(MAKE) migrate

run:
	poetry run uvicorn race_condition.race:app --port 8080 --reload

deploy:
	@$(MAKE) generate_dot_env
	docker-compose build
	docker-compose up -d

migration:
	PYTHONPATH=. poetry run alembic revision --autogenerate

migrate:
	PYTHONPATH=. poetry run alembic upgrade head

generate_dot_env:
	cp -n .env.example .env

codestyle:
	poetry run flake8 app
	poetry run black --check app
	poetry run mypy -p app --namespace-packages

emails:
	yarn run mjml app/templates/emails/src/*.mjml -o app/templates/emails/build/

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build

