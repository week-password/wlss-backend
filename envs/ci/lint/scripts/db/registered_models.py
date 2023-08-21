"""This script is used to compare models existing in repository with models registered in alembic.ini file.

All src/**/models.py files should be added to 'models_packages' inside alembic.ini file.
It will allow alembic to find our models and work with migrations for those models.

So this script can find any models.py file which actually exists in repository but not registered in alembic.ini,
and also find any models.py file which is registered in alembic.ini but does not exist in repository.
"""

import os
import sys
from configparser import ConfigParser
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[5]


def main():
    used_packages = set(get_used_models_packages())
    registered_packages = set(get_registered_models_packages())

    missed_packages = registered_packages - used_packages
    if missed_packages:
        print_missed_packages_error(missed_packages)

    redundant_packages = used_packages - registered_packages
    if redundant_packages:
        print_redundant_packages_error(redundant_packages)

    if not missed_packages and not redundant_packages:
        print("All models registered in alembic.ini correctly.")
        sys.exit(0)

    sys.exit(1)


def get_registered_models_packages():
    """Get models packages registered in 'models_packages' section of alembic.ini file."""
    config = ConfigParser(allow_no_value=True)
    config.read(PROJECT_ROOT / "alembic.ini")

    for package_path in config["alembic"]["models_packages"].split(","):
        package_path = package_path.strip()
        if package_path:
            yield package_path


def get_used_models_packages():
    """Get all models packages existing inside src/ directory."""
    for path in (PROJECT_ROOT / "src").glob("**/models.py"):
        path = str(path.relative_to(PROJECT_ROOT))
        path = path[:-3]  # cut off ".py" extension
        package_path = path.replace(os.sep, ".")
        yield package_path


def print_redundant_packages_error(packages):
    print(
        "\n"
        "ERROR Following packages should be added to 'models_packages' in alembic.ini file\n"
        "since they are used but not registered:"
        "\n"
    )
    print("\n".join(packages), end="\n\n")


def print_missed_packages_error(packages):
    print(
        "\n"
        "ERROR Following packages should be removed from 'models_packages' in alembic.ini file\n"
        "since they are registered but not used:"
        "\n"
    )
    print("\n".join(packages), end="\n\n")


if __name__ == "__main__":
    main()
