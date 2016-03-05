import unittest
import datetime
from webserver.src.main.server import DateTimeManager

# Unit tests for DateTimeManager

class DateTimeTest(unittest.TestCase):

    ''' This test sometimes fails because the milliseconds aren't exact. That is ok because
        both this test and the method we are testing gets the current time, so there may be
        discrepancies in the exact time. '''

    def test_get_begin_date(self):
        dt = DateTimeManager.DateTimeManager()

        # Test with weeks
        d = datetime.timedelta(weeks=3)
        self.assertEqual(dt.get_begin_date("week", 3), (datetime.datetime.now() - d))
        d = datetime.timedelta(weeks=7)
        self.assertEqual(dt.get_begin_date("week", 7), (datetime.datetime.now() - d))
        d = datetime.timedelta(weeks=0)
        self.assertEqual(dt.get_begin_date("week", 0), (datetime.datetime.now() - d))

        # Test with days
        d = datetime.timedelta(days=5)
        self.assertEqual(dt.get_begin_date("day", 5), (datetime.datetime.now() - d))
        d = datetime.timedelta(days=20)
        self.assertEqual(dt.get_begin_date("day", 20), (datetime.datetime.now() - d))
        d = datetime.timedelta(days=0)
        self.assertEqual(dt.get_begin_date("day", 0), (datetime.datetime.now() - d))

        # Test with hours
        d = datetime.timedelta(hours=2)
        self.assertEqual(dt.get_begin_date("hour", 2), (datetime.datetime.now() - d))
        d = datetime.timedelta(hours=23)
        self.assertEqual(dt.get_begin_date("hour", 23), (datetime.datetime.now() - d))
        d = datetime.timedelta(hours=0)
        self.assertEqual(dt.get_begin_date("hour", 0), (datetime.datetime.now() - d))

        # Test with minutes
        d = datetime.timedelta(minutes=45)
        self.assertEqual(dt.get_begin_date("minute", 45), (datetime.datetime.now() - d))
        d = datetime.timedelta(minutes=88)
        self.assertEqual(dt.get_begin_date("minute", 88), (datetime.datetime.now() - d))
        d = datetime.timedelta(minutes=0)
        self.assertEqual(dt.get_begin_date("minute", 0), (datetime.datetime.now() - d))

    def test_get_iso_format(self):
        dt = DateTimeManager.DateTimeManager()
        test_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
        test_iso = "1999-12-31T23:59:59"
        self.assertEqual(dt.get_iso_format(test_date), test_iso)

if __name__ == "__main__":
    unittest.main()