import unittest
import datetime
from reportserver.manager import dateTimeUtility

# Unit tests for DateTimeManager

class DateTimeTest(unittest.TestCase):

    #The date checks ignore milliseconds, since we are just trying to get the correct date.

    def test_get_begin_date(self):


        # Test with weeks
        d = datetime.timedelta(weeks=3)
        self.assertEqual( (dateTimeUtility.get_begin_date("weeks", 3)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(weeks=7)
        self.assertEqual(dateTimeUtility.get_begin_date("weeks", 7), self.getDeltaOfDateNow(d))
        d = datetime.timedelta(weeks=0)
        self.assertEqual(dateTimeUtility.get_begin_date("weeks", 0), self.getDeltaOfDateNow(d))

        # Test with days
        d = datetime.timedelta(days=5)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 5), self.getDeltaOfDateNow(d))
        d = datetime.timedelta(days=20)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 20), self.getDeltaOfDateNow(d) )
        d = datetime.timedelta(days=0)
        self.assertEqual(dateTimeUtility.get_begin_date("days", 0), self.getDeltaOfDateNow(d) )

        # Test with hours
        d = datetime.timedelta(hours=2)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 2),self.getDeltaOfDateNow(d) )
        d = datetime.timedelta(hours=23)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 23), self.getDeltaOfDateNow(d) )
        d = datetime.timedelta(hours=0)
        self.assertEqual(dateTimeUtility.get_begin_date("hours", 0), self.getDeltaOfDateNow(d) )

        # Test with minutes
        d = datetime.timedelta(minutes=45)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 45), self.getDeltaOfDateNow(d) )
        d = datetime.timedelta(minutes=88)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 88), self.getDeltaOfDateNow(d) )
        d = datetime.timedelta(minutes=0)
        self.assertEqual(dateTimeUtility.get_begin_date("minutes", 0),self.getDeltaOfDateNow(d) )

    def getDeltaOfDateNow(self, delta):
        return (datetime.datetime.now() - delta).date()



    def test_get_iso_format(self):

        test_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
        test_iso = "1999-12-31T23:59:59"
        self.assertEqual(dateTimeUtility.get_iso_format(test_date), test_iso)

if __name__ == "__main__":
    unittest.main()