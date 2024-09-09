# aa-Vector-DBs
Add description

## Prerequisites

- Python3.10 is the minimum recommended version installed on your machine.
- VSCODE/Pycharm are the recommended IDEs
- Azure Data Studio/DBeaver/PgAdmin are just some popular DB Clients that can be used with Postgres

## Fork Instructions


## General
1. Project is configured to fail the build if unit test coverage is < 80%. Always make sure to add sufficient tests for your code.
2. Configuration should *only* be done through Annotations

## Setup

- It is recommended to use [pyenv](https://github.com/pyenv/pyenv), a CLI tool that allows multiple versions of Python to be
  installed separately. Follow the [installation instructions](https://github.com/pyenv/pyenv#installation)
  for your platform and run:

  ```
  pyenv install
  ```

- This will download and install Python **3.10.12** which is specified in the `.project-version` file which in turn is created by the command `pyenv local 3.10.12`. This use of pyenv ensures the pinning and usage of the specified Python version.

  > Note: pyenv downloads and compiles the version of Python you install, which means you may need
  > to also install some libraries if not present in your system, please follow the
  > [common build problems wiki](https://github.com/pyenv/pyenv/wiki/Common-build-problems) for
  > your platform.
  >
  > If you already have Python 3.10.12 installed you do not need to reinstall it and pyenv should automatically use the correct version due to the pinning file `.project-version`

- Create a virtualenv:

  ```bash
    python -m venv .venv
    source .venv/bin/activate
  ```
  This virtualenv now has the version of Python which was set by pyenv and the .project-version file.

  > Note: the rest of these instructions assume you've activated the virtualenv as does the Makefile. You may want to use a virtualenv tool like
  > [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) or
  > [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

- Install dependencies via:
  ```bash
  make install-dev
  ```
- Please do not use pip by hand as the makefile contains the explicit activation of pre-commit hooks which will be necessary.

## Testing

### Unit Testing
Tested with python 3.10.12.

```bash
  make install-dev
```

- Run all unit tests with:
```bash
  make unit
 ```
