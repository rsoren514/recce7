import unittest
import sys
from reportserver.manager import utilities

# Unit tests for utililties.py

class Utilities_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_port_number(self):
        result = utilities.validate_port_number("200")
        self.assertEqual(200,result,"expected an integer of 200")

        result = utilities.validate_port_number("abc")
        self.assertEqual(None, result, "expected None")

        result = utilities.validate_port_number(str(sys.maxsize + 100))
        self.assertEqual(sys.maxsize + 100, result, "expected system maxsize + 100")

    def test_validate_time_period(self):
        result = utilities.validate_time_period(["days=1"])
        self.assertEqual(("days",1), result, "expected a tuple of days, 1")

        result = utilities.validate_time_period(["hours=10"])
        self.assertEqual(("hours", 10), result, "expected a tuple of hours, 10")

        result = utilities.validate_time_period(["minutes=10"])
        self.assertEqual(("minutes", 10), result, "expected a tuple of minutes, 10")

        result = utilities.validate_time_period(["weeks=10"])
        self.assertEqual(("weeks", 10), result, "expected a tuple of weeks, 10")

        result = utilities.validate_time_period(["days=1", "years=1"])
        self.assertEqual(("days", 1), result, "expected a tuple of days, 1")

        result = utilities.validate_time_period(["days=1", "weeks=10"])
        self.assertEqual(("days", 1), result, "expected a tuple of days, 1")

        result = utilities.validate_time_period(["weeks=10", "minutes=10"])
        self.assertEqual(("weeks", 10), result, "expected a tuple of weeks, 10")

    def test_get_path_query_tokens(self):
        result = utilities.get_path_query_tokens("/v1/analytics/ports/23")
        answer = ( ["","v1","analytics","ports","23"],[] )
        self.assertSequenceEqual(answer, result, "expected: " + str(answer))

        result = utilities.get_path_query_tokens("/v1/analytics/ports/23?days=1")
        answer = (["", "v1", "analytics", "ports", "23"], ["days=1"])
        self.assertSequenceEqual(answer, result, "expected: " + str(answer))

        result = utilities.get_path_query_tokens("/v1/analytics/ports/23?days=1&minutes=100")
        answer = (["", "v1", "analytics", "ports", "23"], ["days=1","minutes=100"])
        self.assertSequenceEqual(answer, result, "expected: " + str(answer))

        result = utilities.get_path_query_tokens("/v1/analytics/ports/23?foo=bar&minutes=100")
        answer = (["", "v1", "analytics", "ports", "23"], ["foo=bar","minutes=100"])
        self.assertSequenceEqual(answer, result, "expected: " + str(answer))

if __name__ == "__main__":
    unittest.main()