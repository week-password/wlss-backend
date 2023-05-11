# WLSS backend

Backend application for [Wish List Sharing Service](https://github.com/week-password/wisher).

***

## System requirements

To develop this project you need to have the following software installed.

- Docker 19.03+ (as a part of [Docker Desktop](https://docs.docker.com/get-docker/))
- Docker Compose 2.0.0+ (as a part of [Docker Desktop](https://docs.docker.com/get-docker/))
- [Poetry 1.4.2](https://python-poetry.org/docs/)
- [Python](https://www.python.org/) (see version in `pyproject.toml` file)

***

## First time setup

Before start to setup project you have to meet [System requirements](#system-requirements).

Go to the project root directory.

1. Setup git user for this repository.
```bash
source envs/local/dev/scripts/git/iam.sh
```

2. Create virtual environment and install dependencies.
```bash
poetry install
```

3. Activate virtual environment.
```bash
poetry shell
```


## Run app

To run application you need to do all steps from [First time setup](#first-time-setup) section.

1. Run services.
```bash
docker compose --file=envs/local/dev/docker-compose.yml up --detach
```

2. Apply migrations.
```bash
WLSS_ENV=local/dev alembic upgrade head
```

3. Run FastAPI.
```bash
WLSS_ENV=local/dev uvicorn src.app:app
```

# 4. Check health status.
```bash
curl --request GET http://localhost:8000/health
```


## Run linters

To run linters you need to do all steps from [First time setup](#first-time-setup) section.

Linters order below is a preferred way to run and fix them one by one.

1. Mypy.
```bash
mypy
```

2. Ruff.
```bash
ruff check src tests
```

3. Flake8.
```bash
flake8
```

4. Pylint.
```bash
pylint src tests
```


## Run tests

To run tests you need to do all steps from [First time setup](#first-time-setup) section.

1. Run services.
```bash
docker compose --file=envs/local/test/docker-compose.yml up --detach
```

2. Apply migrations.
```bash
WLSS_ENV=local/test alembic upgrade head
```

- Pytest.
```bash
WLSS_ENV=local/test pytest --cov=src
```

- Coverage report.
```bash
coverage html
```

- Report with contexts.
```bash
WLSS_ENV=local/test pytest --cov=src --cov-context=test ; coverage html --show-contexts --no-skip-covered
```

## Working with migrations

Following examples will use `local/test` environment, but you can use any other value for `$WLSS_ENV` you need.

- Generate new migration.
```bash
WLSS_ENV=local/test alembic revision --autogenerate -m "migration message"
```

- Apply all migrations.
```bash
WLSS_ENV=local/test alembic upgrade head
```

- Apply migrations up to particular revision.
```bash
WLSS_ENV=local/test alembic upgrade 746039e79eb3
```

- Downgrade certain number of migrations.
```bash
WLSS_ENV=local/test alembic downgrade -2
```

- Downgrade migrations to particular revision.
```bash
WLSS_ENV=local/test alembic upgrade 746039e79eb3
```

- Autoformat revision code if you changed it by hand.
```bash
black --line-length=120 migrations
```


## Troubleshooting

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
