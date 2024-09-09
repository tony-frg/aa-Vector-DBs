## ATTENTION! activate virtual environment before running!

##  install packages, install pre-commit
install-dev:
	pip3 install -U pip wheel setuptools
	pip3 install -r requirements-dev.txt
	pre-commit install
	opentelemetry-bootstrap -a install


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +


clean-test:
	rm -rf .coverage
	rm -rf .coverage.*
	rm -rf coverage-reports
	rm -rf allure_results


clean: clean-pyc clean-test


## uninstall all dev packages
uninstall-dev:
	pip freeze | xargs pip uninstall -y


## Run linting checks
check:
	isort --check src tests	# setup.cfg
	black --check src tests	# pyproject.toml
	flake8 src tests	# setup.cfg
	mypy src tests	# setup.cfg


## reformat the files using the formatters
format:
	isort src tests
	black src tests


## down build docker image
drop-image:
	docker compose -f docker-compose-test.yaml down -v --rmi all


## build docker image
build-image:
	docker compose -f docker-compose-test.yaml build


## run docker image
run-image:
	docker compose -f docker-compose-test.yaml up -d


## drop containers
drop-containers:
	docker compose -f docker-compose-test.yaml down --volumes --remove-orphans


## run unit tests
unit: clean
	pytest -v -s tests/unit --no-header -vv --cov=src --cov-report=term-missing
	coverage xml

## spin up local environment
local-environment:
	sh ci_scripts/setup_integration_environment.sh

## remove api docker image
local-environment-teardown:
	echo "Drop all docker containers"
	make drop-containers

	echo "Remove staff recommender service api docker image"
	docker rmi -f "staff-recommender-service-api:latest"

## run integration tests
integration:
	make local-environment

	python -m pytest -v tests/integration --alluredir=allure_results || (make local-environment-teardown && exit 1)

	make local-environment-teardown
	make clean

functional:
	python -m pytest -v tests/functional
	make clean

api-tests:
	python -m pytest -v tests/api
mypy:
	. .venv/bin/activate && mypy src


lint:
	. .venv/bin/activate && pylint src -j 4 --reports=y


docs: FORCE
	cd docs; . .venv/bin/activate && sphinx-apidoc -o ./source ./src
	cd docs; . .venv/bin/activate && sphinx-build -b html ./source ./build
FORCE:


migrations:
	cd src/infra; alembic upgrade heads
