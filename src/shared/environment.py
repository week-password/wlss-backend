"""Utilities for working with environment variables."""

import os
from typing import Final

from dotenv import load_dotenv

from src import PROJECT_ROOT


def load_environment() -> None:  # pragma: no cover
    """Load environment variables from dotenv file provided via $WLSS_ENV environment variable.

    The value of $ENV variable should be one of those (listed in resolution order):
        - path to a directory containing `.env` file relative to `PROJECT_ROOT/envs/`
        - path to a dotenv file relative to `PROJECT_ROOT/envs/`
        - path to a directory containing `.env` file relative to `PROJECT_ROOT/`
        - path to a dotenv file relative to `PROJECT_ROOT/`

    :raises InvalidEnvironment:  raised if $WLSS_ENV environment variable isn't set
    """
    if "WLSS_ENV" not in os.environ:
        msg = "Cannot load environment variables. Please define $WLSS_ENV environment variable."
        raise InvalidEnvironment(msg)

    WLSS_ENV: Final = os.environ["WLSS_ENV"]  # noqa: N806

    envs_relative_path = PROJECT_ROOT / "envs" / WLSS_ENV
    root_relative_path = PROJECT_ROOT / WLSS_ENV
    dotenv_path = envs_relative_path if envs_relative_path.exists() else root_relative_path

    if dotenv_path.is_dir():
        dotenv_path = dotenv_path / ".env"
    load_dotenv(dotenv_path, override=True)


class InvalidEnvironment(Exception):  # noqa: N818
    """Raised if there were errors during environment variables loading."""
