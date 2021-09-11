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
        {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": b'365'},
        {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": b'1'},
        {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": b'1'},
        {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": b'30'},
        {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": b'366'},
        {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": b'0'},
        {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": b'-365'},
    ]

    for data in test_data:
        rv = client.get('/days?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
        assert data.get("result") in rv.data


def test_weekdays(client):
    """Test the correct number of weekdays is returned from two dates"""
    test_data = [
        {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": b'261'},
        {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": b'1'},
        {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": b'0'},
        {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": b'21'},
        {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": b'261'},
        {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": b'0'},
        {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": b'-261'},
    ]

    for data in test_data:
        rv = client.get('/weekdays?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
        assert data.get("result") in rv.data


def test_completeweeks(client):
    """Test the correct number of weekdays is returned from two dates"""
    test_data = [
        {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": b'52'},
        {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": b'0'},
        {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": b'0'},
        {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": b'4'},
        {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": b'52'},
        {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": b'0'},
        {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": b'-52'},
    ]

    for data in test_data:
        rv = client.get('/completeweeks?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
        assert data.get("result") in rv.data