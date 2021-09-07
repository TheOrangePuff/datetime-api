import pytest

from datetime_api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_test(client):
    """Testing tests."""

    rv = client.get('/')
    assert b'Hello World' in rv.data
