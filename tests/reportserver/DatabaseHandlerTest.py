import unittest
import sqlite3
import os
import datetime
import shutil

from common.globalconfig import Configuration
from reportserver.dao import DatabaseHandler
from database import DB_Init

class DatabaseHandlerTest(unittest.TestCase):

    # Creates a test DB with 1 table and 1000 entries with different timestamps.
    def setUp(self):
        conn = sqlite3.connect("TestDB.sqlite")
        c = conn.cursor()
        c.execute('''CREATE TABLE Dates (col1 text, col2 text, eventDateTime text)''')
        test_start_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)

        for x in range(0, 1000):
            d = datetime.timedelta(weeks=x)
            insert_date = (test_start_date + d)
            insert_date_iso = insert_date.isoformat()
            c.execute("INSERT INTO Dates VALUES ('TEXT1','TEXT2','%s')" % insert_date_iso)

        conn.commit()

    # Tests connecting to the DB. Includes testing for incorrect paths.
    def test_connect(self):
        # Negative testing
        self.assertIsNone(DatabaseHandler.connect("database"))
        self.assertIsNone(DatabaseHandler.connect("database.db"))
        self.assertIsNone(DatabaseHandler.connect("asdl;kfjeiei"))
        self.assertIsNone(DatabaseHandler.connect("./honeyDB/honeyDB.sqllite"))
        self.assertIsNone(DatabaseHandler.connect("./honeyDB/honeyDB.db"))
        self.assertIsNone(DatabaseHandler.connect(" "))
        self.assertIsNone(DatabaseHandler.connect(""))

        # Testing for correct DB
        cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
        global_config = Configuration(cfg_path).getInstance()
        DB_Init.create_db_dir(global_config)
        DB_Init.create_db(global_config)
        db_path = global_config.get_db_dir() + '/honeyDB.sqlite'

        self.assertTrue(sqlite3.connect(db_path))
        self.assertTrue(DatabaseHandler.connect(db_path))
        self.assertTrue(DatabaseHandler.connect())
        shutil.rmtree('honeyDB')

    # TODO - MORE TESTS!!!
    def test_query_db(self):
        test_start_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
#        successes = 0
#        fails = 0
        for x in range(0, 1000):
            d = datetime.timedelta(weeks=x)
            query_date = (test_start_date + d)
            query_date_iso = query_date.isoformat()
            query_string = "SELECT * FROM Dates where (eventDateTime >= '%s')" % query_date_iso
            json_query = DatabaseHandler.query_db(query_string, db = "TestDB.sqlite")
            for y in range(0, len(json_query) - 1):
                date = json_query[y].get('eventDateTime')
                self.assertGreaterEqual(date, query_date_iso)
#                if date >= query_date_iso:
#                    successes += 1
#                else:
#                    fails += 1
#            with open("test_query_log.txt", "a") as log:
#                log.write("Tested %s, had %d successes and %d fails\n" % (query_date_iso, successes, fails))
#            successes = 0
#            fails = 0

    # TODO - MORE TESTS!!!
    def test_get_json_by_time(self):
        query = DatabaseHandler.get_json_by_time("Dates", "weeks", 150)
        expected = [
            {"title": "Castlevania: Lords of Shadow 2", "datetime": "2014-02-25T00:00:00", "system": "PlayStation 3"},
            {"title": "Castlevania: Lords of Shadow 2", "datetime": "2014-02-25T00:00:00", "system": "Xbox 360"}
        ]
        self.assertEqual(query, expected)

#    def jsonstr(self, json_dict):
#        str_json = str(json_dict)
#        return str_json.replace("'", "\"")

    def tearDown(self):
        os.remove("TestDB.sqlite")

if __name__ == "__main__":
    unittest.main()