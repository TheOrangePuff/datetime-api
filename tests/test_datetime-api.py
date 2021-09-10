import pytest

from datetime_api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_days(client):
    """Test the correct number of days is returned from two dates"""
    test_data = [
        {"date1": "2021-01-01", "date2": "2022-01-01", "result": b'365'},
        {"date1": "2021-01-01", "date2": "2021-01-31", "result": b'30'},
        {"date1": "1984-01-01", "date2": "1985-01-01", "result": b'366'},
        {"date1": "2021-01-01", "date2": "2021-01-01", "result": b'0'},
    ]

    for data in test_data:
        rv = client.get('/days?date1=' + data.get("date1") + '&date2=' + data.get("date2"))
        assert data.get("result") in rv.data
