from src.routes import route


def test_session_routes_with_mocked_session_returns_mocked_session():
    result = route()

    # this would be `result == "some-session"` if our mock haven't been applied
    assert result == "mocked-session"
