import functools


def session(session_fn):
    """This is the actual decorator for providing session to routes/repositories/whatever."""
    def _get_session(fn):
        @functools.wraps(fn)
        def newfn(*args, **kwargs):
            if kwargs.get("session"):
                return fn(*args, **kwargs)

            kwargs["session"] = session_fn
            return fn(*args, **kwargs)

        return newfn
    return _get_session
