import functools


class KwargsBuilder:
    """This class may look like "Builder" pattern, but it is not actually.

    Here it is used only for patching convenience.
    It's relatively easy to use `patch.object` instead of regular `patch`
    because `patch.object` doesn't depend on "calling path".
    So we can just import this class anywhere we want to use `patch.object`
    and just patch the exact method we want.
    """

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def with_session(self, session):
        if self.kwargs.get("session"):
            return self.kwargs
        self.kwargs["session"] = session
        return self.kwargs


def session(session_fn):
    """This is the actual decorator for providing session to routes/repositories/whatever."""
    def _get_session(fn):
        @functools.wraps(fn)
        def newfn(*args, **kwargs):
            kwargs = KwargsBuilder(kwargs).with_session(session_fn)
            return fn(*args, **kwargs)

        return newfn
    return _get_session
