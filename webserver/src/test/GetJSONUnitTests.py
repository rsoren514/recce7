import unittest
import sqlite3

from webserver.src.main.server import GetJSON

class GetJSONTests(unittest.TestCase):

    # GetJSON function should return the DB location from config file.
    def db_test(self):
        gj = GetJSON.Getjson()
        # will need location of DB for this test
        db1 = sqlite3.connect("DB.db")
        db2 = gj.db()
        self.assertEqual(db1, db2)

    def query_db_test(self):
        gj = GetJSON.Getjson()

    def getjson_test(self):
        gj = GetJSON.Getjson()