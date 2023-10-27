from unittest.mock import patch

from src.session import KwargsBuilder
from src.routes import route


def with_session_mock(self, default_session):
    self.kwargs["session"] = "mocked-session"
    return self.kwargs


def test_session_routes_with_mocked_session_returns_mocked_session():
    with patch.object(KwargsBuilder, "with_session", with_session_mock):

        result = route()

    # this would be `result == "some-session"` if our mock haven't been applied
    assert result == "mocked-session"
