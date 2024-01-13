# WLSS backend

![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/birthdaysgift/4fc310fa76bff267f6b9f1c9d00c812b/raw/mypy.json)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/birthdaysgift/4fc310fa76bff267f6b9f1c9d00c812b/raw/ruff.json)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/birthdaysgift/4fc310fa76bff267f6b9f1c9d00c812b/raw/flake8.json)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/birthdaysgift/4fc310fa76bff267f6b9f1c9d00c812b/raw/pylint.json)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/birthdaysgift/4fc310fa76bff267f6b9f1c9d00c812b/raw/pytest.json)


Backend application for [Wish List Sharing Service](https://github.com/week-password/wisher).


## Table of Contents

[System requirements](#system-requirements)

[First time setup](#first-time-setup)

[Run app](#run-app)

[Run linters](#run-linters)

[Run tests](#run-tests)

[Working with migrations](#working-with-migrations)

[Deploy](#deploy)

[Troubleshooting](#troubleshooting)


***


## [System requirements](#table-of-contents)

To develop this project you need to have the following software installed.

- Docker 19.03+ (as a part of [Docker Desktop](https://docs.docker.com/get-docker/))
- Docker Compose 2.0.0+ (as a part of [Docker Desktop](https://docs.docker.com/get-docker/))
- [Poetry 1.4.2](https://python-poetry.org/docs/)
- [Python](https://www.python.org/) (see version in `pyproject.toml` file)


## [First time setup](#table-of-contents)

Before start to setup project you have to meet [System requirements](#system-requirements).

Go to the project root directory.

1. Set up local environment:
```bash
# Set up git user for this repository
source envs/local/dev/scripts/git/iam.sh

# Create virtual environment and install dependencies.
poetry install --with app,lint,test

# Activate virtual environment.
poetry shell
```

2. Upgrade pip within virtual environment:
```bash
pip install --upgrade pip
```


## [Run app](#table-of-contents)

To run application you need to do all steps from [First time setup](#first-time-setup) section.

1. Run services and app:
```bash
# Create .env file
source envs/local/dev/env.sh

# Run services.
docker compose --file=envs/local/dev/docker-compose.yml up --detach

# Apply migrations.
WLSS_ENV=local/dev alembic upgrade head

# Run development server.
WLSS_ENV=local/dev uvicorn src.app:app --reload
```

2. Check application health status:
```bash
curl --request GET http://localhost:8000/health
```


## [Run linters](#table-of-contents)

To run linters you need to do all steps from [First time setup](#first-time-setup) section.

Linters order below is a preferred way to run and fix them one by one.

Run any linter you need or all of them at once:
```bash
# Run mypy.
mypy

# Run ruff.
ruff check src tests

# Run flake8.
flake8

# Run pylnig.
pylint src tests
```


## [Run tests](#table-of-contents)

To run tests you need to do all steps from [First time setup](#first-time-setup) section.

1. Run services and tests:
```bash
# Create .env file
source envs/local/test/env.sh

# Run services.
docker compose --file=envs/local/test/docker-compose.yml up --detach

# Apply migrations.
WLSS_ENV=local/test alembic upgrade head

# Run pytest.
WLSS_ENV=local/test pytest --cov=src
```

Also you can choose one of the following ways of running tests:

- Tests with html coverage report:
```bash
WLSS_ENV=local/test pytest --cov=src ; coverage html
```

- Tests with execution contexts in report:
```bash
WLSS_ENV=local/test pytest --cov=src --cov-context=test ; coverage html --show-contexts --no-skip-covered
```


## [Working with migrations](#table-of-contents)

Following examples will use `local/test` environment, but you can use any other value for `$WLSS_ENV` you need.

- Generate new migration:
```bash
WLSS_ENV=local/test alembic revision --autogenerate -m "migration message"
```

- Apply all migrations:
```bash
WLSS_ENV=local/test alembic upgrade head
```

- Apply migrations up to particular revision:
```bash
WLSS_ENV=local/test alembic upgrade 746039e79eb3
```

- Downgrade certain number of migrations:
```bash
WLSS_ENV=local/test alembic downgrade -2
```

- Downgrade migrations to particular revision:
```bash
WLSS_ENV=local/test alembic upgrade 746039e79eb3
```

- Autoformat revision code if you changed it by hand:
```bash
black --line-length=120 migrations
```


## [Deploy](#table-of-contents)

_Only users with write access are able to deploy._

1. Fetch the last version of the `deployed/qa` tag:
```bash
git fetch origin +refs/tags/deployed/qa:refs/tags/deployed/qa
```

2. Checkout to branch/commit you want to deploy.

3. Create and push new version of the `deployed/qa` tag:
```bash
git tag --annotate --force deployed/qa --message ''
git push origin deployed/qa --force
```


## [Troubleshooting](#table-of-contents)

***

**Problem:**

For mac users, if you have some issues with pylint's spellchecker, for example:
```text
optparse.OptionValueError: option spelling-dict: invalid value: 'en_US', should be in ['']
```

**Solution:**

Install `enchant` system-wide (see [this](https://stackoverflow.com/a/27162411/8431075)):
```bash
brew install enchant
```

Or if you have an Apple Siliicon Chip (see [this](https://stackoverflow.com/a/73052239/8431075)), then you should run:
```bash
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
arch -x86_64 /usr/local/bin/brew install enchant
```
and then setting the environment variable:
```bash
export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib
```

***
