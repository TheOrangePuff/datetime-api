import unittest

from datetime_api import create_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_days(self):
        """Test the correct number of days is returned from two dates"""
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": b'365'},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": b'1'},
            {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": b'1'},
            {"start_date": "2020-12-31", "end_date": "2021-01-01", "result": b'1'},
            {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": b'30'},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": b'366'},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": b'0'},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": b'-365'},
        ]

        for data in test_data:
            rv = self.app.get('/days?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
            assert data.get("result") in rv.data

    def test_days_units(self):
        """
        Test the correct number of seconds, minutes, hours or years is returned
        from two dates
        """
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "seconds", "result": b'31536000'},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "seconds", "result": b'86400'},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "seconds", "result": b'31622400'},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": b'0'},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": b'-31536000'},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "minutes", "result": b'525600'},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "minutes", "result": b'1440'},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "minutes", "result": b'527040'},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": b'0'},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": b'-525600'},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "hours", "result": b'8760'},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "hours", "result": b'24'},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "hours", "result": b'8784'},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "hours", "result": b'0'},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "hours", "result": b'-8760'},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "years", "result": b'1'},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "years", "result": b'0'},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "years", "result": b'1'},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "years", "result": b'0'},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "years", "result": b'-1'},
        ]

        for data in test_data:
            rv = self.app.get('/days?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date")
                              + '&unit=' + data.get("unit"))
            assert data.get("result") in rv.data

    def test_weekdays(self):
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
            rv = self.app.get('/weekdays?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
            assert data.get("result") in rv.data

    def test_completeweeks(self):
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
            rv = self.app.get(
                '/completeweeks?start_date=' + data.get("start_date") + '&end_date=' + data.get("end_date"))
            assert data.get("result") in rv.data
