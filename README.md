# Wisher backend

***

## System requirements

To develop this project you need to have the following software installed.

- [Poetry 1.4.2](https://python-poetry.org/docs/)
- [Python](https://www.python.org/) (see version in `pyproject.toml` file)

***

## First time setup

Before start to setup project you have to meet [System requirements](#system-requirements).

Go to the project root directory.

1. Setup git user for this repository.
```bash
source envs/dev/scripts/git/iam.sh
```

2. Create virtual environment and install dependencies.
```bash
poetry install
```

3. Activate virtual environment.
```bash
poetry shell
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
ruff check src
```

3. Flake8.
```bash
flake8
```

4. Pylint.
```bash
pylint src
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
