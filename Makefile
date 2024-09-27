## ATTENTION! activate virtual environment before running!

##  install packages, install pre-commit
install-dev:
	pip3 install -U pip wheel setuptools
	pip3 install --no-cache-dir --upgrade -r requirements-dev.txt
	pre-commit install


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +


clean: clean-pyc


## uninstall all dev packages
uninstall-dev:
	pip freeze | xargs pip uninstall -y


## Run linting checks
check:
	isort --check src # setup.cfg
	black --check src # pyproject.toml
	flake8 src 		  # setup.cfg
	mypy src          # setup.cfg


## reformat the files using the formatters
format:
	isort src
	black src


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
