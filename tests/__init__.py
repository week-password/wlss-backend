"""Main package for all tests."""

import functools
from unittest.mock import patch

from src import session


def mocked_session(session_fn):
    """This decorator replacess actual session decorator to provide mocked-session into routes/repositories/whatever."""
    def _get_session(fn):
        @functools.wraps(fn)
        def newfn(*args, **kwargs):
            kwargs["session"] = "mocked-session"
            return fn(*args, **kwargs)

        return newfn
    return _get_session


patch.object(session, "session", mocked_session).start()
