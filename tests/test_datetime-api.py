import unittest
import json

from datetime_api import create_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def build_url(self, base_url, data):
        """Build a test url given a base url and data"""
        url = base_url + "?start_date=" + data.get("start_date") \
                       + "&end_date=" + data.get("end_date")

        if data.get("unit"):
            url += '&unit=' + data.get("unit")

        return url

    def get_test_result(self, response, data):
        """Run the test for the given response and data"""
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['difference'], data.get("result"),
                         "Test failed for: " + str(data))

    def run_test_get(self, base_url, test_data):
        """Function to test GET responses"""
        for data in test_data:
            url = self.build_url(base_url, data)
            response = self.app.get(url)

            self.get_test_result(response, data)

    def run_test_post(self, base_url, test_data):
        """Function to test POST responses"""
        for data in test_data:
            url = self.build_url(base_url, data)
            response = self.app.post(url)

            self.get_test_result(response, data)

    def test_days(self):
        """Test the correct number of days is returned from two dates"""
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": 365},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": 1},
            {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": 1},
            {"start_date": "2020-12-31", "end_date": "2021-01-01", "result": 1},
            {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": 30},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": 366},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": -365},
        ]

        self.run_test_get("days", test_data)
        self.run_test_post("days", test_data)

    def test_days_timezone(self):
        """Test the correct number of days is returned from two dates"""
        test_data = [
            {"start_date": "2020-12-31T2300%2B0100", "end_date": "2022-01-01T1030-1030", "result": 365},
            {"start_date": "2021-01-01T0100-0100", "end_date": "2021-01-02T1030-1030", "result": 1},
            {"start_date": "2022-01-01T0100-0100", "end_date": "2021-01-01T1030-1030", "result": -365},
            {"start_date": "2021-01-01T0100-0100", "end_date": "2021-01-01T1030-1030", "result": 0},
            {"start_date": "2021-01-01-0100", "end_date": "2021-01-01", "unit": "hours", "result": -1},
        ]

        self.run_test_get("days", test_data)
        self.run_test_post("days", test_data)

    def test_days_units(self):
        """
        Test the correct number of seconds, minutes, hours or years is returned
        from two dates
        """
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "seconds", "result": 31536000},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "seconds", "result": 86400},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "seconds", "result": 31622400},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": -31536000},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "minutes", "result": 525600},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "minutes", "result": 1440},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "minutes", "result": 527040},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": -525600},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "hours", "result": 8760},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "hours", "result": 24},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "hours", "result": 8784},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "hours", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "hours", "result": -8760},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "weeks", "result": 52.142857142857146},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "weeks", "result": 0.14285714285714285},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "weeks", "result": 52.285714285714285},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "weeks", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "weeks", "result": -52.142857142857146},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "years", "result": 1},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "years", "result": 0.0027397260273972603},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "years", "result": 1.0027397260273972603},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "years", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "years", "result": -1},
        ]

        self.run_test_get("days", test_data)
        self.run_test_post("days", test_data)

    def test_weekdays(self):
        """Test the correct number of weekdays is returned from two dates"""
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": 261},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": 1},
            {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": 0},
            {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": 21},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": 261},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": -261},
        ]

        self.run_test_get("weekdays", test_data)
        self.run_test_post("weekdays", test_data)

    def test_weekdays_units(self):
        """
        Test the correct number of seconds, minutes, hours or years is returned
        from two dates
        """
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "seconds", "result": 22550400},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "seconds", "result": 86400},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "seconds", "result": 22550400},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": -22550400},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "minutes", "result": 375840},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "minutes", "result": 1440},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "minutes", "result": 375840},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": -375840},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "hours", "result": 6264},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "hours", "result": 24},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "hours", "result": 6264},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "hours", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "hours", "result": -6264},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "weeks", "result": 37.285714285714285},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "weeks", "result": 0.14285714285714285},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "weeks", "result": 37.285714285714285},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "weeks", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "weeks", "result": -37.285714285714285},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "years", "result": 0.7150684931506849},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "years", "result": 0.0027397260273972603},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "years", "result": 0.7150684931506849},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "years", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "years", "result": -0.7150684931506849},
        ]

        self.run_test_get("weekdays", test_data)
        self.run_test_post("weekdays", test_data)

    def test_completeweeks(self):
        """Test the correct number of weekdays is returned from two dates"""
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "result": 52},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "result": 0},
            {"start_date": "2021-01-02", "end_date": "2021-01-03", "result": 0},
            {"start_date": "2021-01-01", "end_date": "2021-01-31", "result": 4},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "result": 52},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "result": -52},
        ]

        self.run_test_get("completeweeks", test_data)
        self.run_test_post("completeweeks", test_data)

    def test_completeweeks_units(self):
        """
        Test the correct number of seconds, minutes, hours or years is returned
        from two dates
        """
        test_data = [
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "seconds", "result": 31449600},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "seconds", "result": 0},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "seconds", "result": 31449600},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "seconds", "result": -31449600},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "minutes", "result": 524160},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "minutes", "result": 0},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "minutes", "result": 524160},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "minutes", "result": -524160},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "hours", "result": 8736},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "hours", "result": 0},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "hours", "result": 8736},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "hours", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "hours", "result": -8736},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "days", "result": 364},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "days", "result": 0},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "days", "result": 364},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "days", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "days", "result": -364},
            {"start_date": "2021-01-01", "end_date": "2022-01-01", "unit": "years", "result": 0.9972602739726028},
            {"start_date": "2021-01-01", "end_date": "2021-01-02", "unit": "years", "result": 0},
            {"start_date": "1984-01-01", "end_date": "1985-01-01", "unit": "years", "result": 0.9972602739726028},
            {"start_date": "2021-01-01", "end_date": "2021-01-01", "unit": "years", "result": 0},
            {"start_date": "2022-01-01", "end_date": "2021-01-01", "unit": "years", "result": -0.9972602739726028},
        ]

        self.run_test_get("completeweeks", test_data)
        self.run_test_post("completeweeks", test_data)
