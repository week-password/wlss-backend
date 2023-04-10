from src.ping import ping


def test_ping_returns_correctly():
    result = ping()

    assert result == "pong"
