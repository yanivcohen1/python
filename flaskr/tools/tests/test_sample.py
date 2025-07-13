# all tested need to be in format test_*.py
# in file setup.cfg in section [tool:pytest] testpaths=flaskr/tools/tests
# in settings.json
"""
"python.testing.pytestEnabled": true,
"python.testing.unittestEnabled": false,
"python.testing.pytestArgs": [
  "flaskr/tools/tests"
]
"""
# run the all tests ">pytest"
# run the spcific tests ">pytest -q test_class.py"
# from testing tab select tests to run or debug
import unittest
from unittest import mock
from unittest.mock import call, patch, ANY
from flaskr.tools.tests.sample import random_sum, silly


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Code to set up class-wide fixtures
        cls.shared_resource = "Shared Resource"
        print("setUpClass: Shared resource initialized")

    @classmethod
    def tearDownClass(cls):
        # Code to clean up class-wide fixtures
        cls.shared_resource = None
        print("tearDownClass: Shared resource cleaned up")

    def setUp(self):
        # Code to set up test fixtures Runs once before any test methods in the class
        self.resource = "SetUp Resource"
        print("setUp: Resource initialized")

    def tearDown(self):
        # Code to tear down test fixtures Runs once after any test methods in the class
        self.resource = None
        print("tearDown: Resource cleaned up")

    @patch("flaskr.tools.tests.sample.random.randint")
    def test_random_sum(self, mock_randint):
        mock_randint.side_effect = [3, 4]  # first run return 3 second run return 4
        assert random_sum() == 7
        mock_randint.assert_has_calls(calls=[call(1, 10), call(1, 7)])

    def my_side_effect(self, num1, num2):
        return num2 + 1

    @patch("flaskr.tools.tests.sample.random")
    def test_my_random_sum(self, mock_random):
        mock_random.randint.side_effect = self.my_side_effect
        assert random_sum() == 19
        mock_random.randint.assert_has_calls(calls=[call(1, 10), call(ANY, ANY)])

    @patch("flaskr.tools.tests.sample.random.randint")
    @patch("flaskr.tools.tests.sample.time.time")
    @patch("flaskr.tools.tests.sample.requests.get")
    def test_silly(self, mock_requests_get, mock_time, mock_randint):
        test_params = {"timestamp": 123, "number": 5}
        mock_time.return_value = test_params["timestamp"]
        mock_randint.return_value = 5
        mock_requests_get.return_value = mock.Mock(
            **{"status_code": 200, "json.return_value": {"args": test_params}}
        )  # all fun need return_value
        assert silly() == test_params

    def my_str(self, strs):
        return strs

    @patch("flaskr.tools.tests.sample.my_str")
    def test_my_random_sum2(self, mock_my_str):
        mock_my_str.side_effect = self.my_str
        assert random_sum() == "mock"
        mock_my_str.assert_has_calls(calls=[call("mock")])

    @patch("flaskr.tools.tests.sample.random.randint")
    @patch("flaskr.tools.tests.sample.time.time")
    @patch("flaskr.tools.tests.sample.requests.get")
    def test_silly2(self, mock_requests_get, mock_time, mock_randint):
        test_params = {"timestamp": 123, "number": 5}
        mock_time.return_value = test_params["timestamp"]
        mock_randint.return_value = test_params["number"]
        req_get_ret_val = mock_requests_get.return_value
        req_get_ret_val.status_code = 200
        req_get_ret_val.json.return_value = {
            "args": test_params
        }  # all fun need return_value
        assert silly() == test_params

    @patch("flaskr.tools.tests.sample.random.randint")
    @patch("flaskr.tools.tests.sample.time.time")
    def test_silly3(self, mock_time, mock_randint):
        test_params = {"timestamp": '123', "number": '5'}
        mock_time.return_value = int(test_params["timestamp"])
        mock_randint.return_value = int(test_params["number"])
        assert silly() == test_params # this will actualy get from the url
