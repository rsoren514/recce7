import unittest
import datetime
from manager import dateTimeUtility

# Unit tests for dateTimeUtility

class DateTimeTest(unittest.TestCase):

    ''' This test sometimes fails because the milliseconds aren't exact. That is ok because
        both this test and the method we are testing gets the current time, so there may be
        discrepancies in the exact time. '''

    def test_get_begin_date(self):

        # Test with weeks
        d = datetime.timedelta(weeks=3)
        self.assertEqual(dateTimeUtility.get_begin_date("weeks", 3), (datetime.datetime.now() - d))
        d = datetime.timedelta(weeks=7)
        self.assertEqual(dateTimeUtility.get_begin_date("weeks", 7), (datetime.datetime.now() - d))
        d = datetime.timedelta(weeks=0)
        self.assertEqual(dateTimeUtility.get_begin_date("weeks", 0), (datetime.datetime.now() - d))

        # Test with days
        d = datetime.timedelta(days=5)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 5), (datetime.datetime.now() - d))
        d = datetime.timedelta(days=20)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 20), (datetime.datetime.now() - d))
        d = datetime.timedelta(days=0)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 0), (datetime.datetime.now() - d))
        d = datetime.timedelta(days=1)
        self.assertEqual(dateTimeUtility.get_begin_date(unit="days"), (datetime.datetime.now() - d))
        self.assertEqual(dateTimeUtility.get_begin_date(), (datetime.datetime.now() - d))

        # Test with hours
        d = datetime.timedelta(hours=2)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 2), (datetime.datetime.now() - d))
        d = datetime.timedelta(hours=23)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 23), (datetime.datetime.now() - d))
        d = datetime.timedelta(hours=0)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 0), (datetime.datetime.now() - d))

        # Test with minutes
        d = datetime.timedelta(minutes=45)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 45), (datetime.datetime.now() - d))
        d = datetime.timedelta(minutes=88)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 88), (datetime.datetime.now() - d))
        d = datetime.timedelta(minutes=0)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 0), (datetime.datetime.now() - d))

        # Test default (1 day)
        d = datetime.timedelta(days=1)
        self.assertEqual(dateTimeUtility.get_begin_date("decades", 45), (datetime.datetime.now() - d))
        self.assertEqual(dateTimeUtility.get_begin_date("iemclaiejfkd djeaa", 2), (datetime.datetime.now() - d))
        self.assertEqual(dateTimeUtility.get_begin_date("", 30), (datetime.datetime.now() - d))
        self.assertEqual(dateTimeUtility.get_begin_date(), (datetime.datetime.now() - d))

    def test_get_iso_format(self):
        test_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
        test_iso = "1999-12-31T23:59:59"
        self.assertEqual(dateTimeUtility.get_iso_format(test_date), test_iso)

if __name__ == "__main__":
    unittest.main()