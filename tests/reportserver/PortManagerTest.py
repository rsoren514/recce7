import unittest

from common.GlobalConfig import Configuration

from reportserver.manager.PortManager import PortManager

# Unit tests for PortManager

class PortManagerTest(unittest.TestCase):

    def test_get_date_delta(self):
        Configuration("./testconfig").getInstance()
        unit = PortManager()

        #one hour different
        test_iso_from = "1999-12-31T22:59:59"
        test_iso_to = "1999-12-31T23:59:59"
        expected_delta = "1:00:00"
        self.assertEqual(unit.get_date_delta(test_iso_from, test_iso_to), expected_delta)

        #the same
        test_iso_from = "1999-12-31T22:59:59"
        test_iso_to = "1999-12-31T22:59:59"
        expected_delta = "0:00:00"
        self.assertEqual(unit.get_date_delta(test_iso_from, test_iso_to), expected_delta)


if __name__ == "__main__":
    unittest.main()