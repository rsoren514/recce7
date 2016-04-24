import unittest
import sqlite3
import os
import datetime
import shutil

from common.globalconfig import GlobalConfig
from reportserver.dao.DatabaseHandler import DatabaseHandler
from database.database import Database

class DatabaseHandlerTest(unittest.TestCase):

    # Creates a test DB with 1 table and 1000 entries with different timestamps.
    def setUp(self):
        conn = sqlite3.connect("TestDB.sqlite")
        c = conn.cursor()
        c.execute('''CREATE TABLE test_http (port int, data text, eventDateTime text)''')
        c.execute('''CREATE TABLE test_http2 (port int, data text, eventDateTime text)''')
        c.execute('''CREATE TABLE test_telnet (port int, data text, eventDateTime text)''')
        test_start_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)

        for x in range(0, 500):
            d = datetime.timedelta(weeks=x)
            insert_date = (test_start_date + d)
            insert_date_iso = insert_date.isoformat()
            c.execute("INSERT INTO test_http VALUES (8082,'TEXT','%s')" % insert_date_iso)
            c.execute("INSERT INTO test_http2 VALUES (8083,'TEXT','%s')" % insert_date_iso)
            c.execute("INSERT INTO test_telnet VALUES (8023,'TEXT','%s')" % insert_date_iso)

        conn.commit()

    # Tests connecting to the DB. Includes testing for incorrect paths.
    def test_connect(self):
        # Negative testing
        self.assertIsNone(DatabaseHandler().connect("database"))
        self.assertIsNone(DatabaseHandler().connect("database.db"))
        self.assertIsNone(DatabaseHandler().connect("asdl;kfjeiei"))
        self.assertIsNone(DatabaseHandler().connect("./honeyDB/honeyDB.sqllite"))
        self.assertIsNone(DatabaseHandler().connect("./honeyDB/honeyDB.db"))
        self.assertIsNone(DatabaseHandler().connect(" "))
        self.assertIsNone(DatabaseHandler().connect(""))

        # Testing for correct DB
        plugin_cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
        global_cfg_path = os.getenv('RECCE7_GLOBAL_CONFIG') or 'config/global.cfg'
        global_config = GlobalConfig(plugin_cfg_path, global_cfg_path, True)
        db = Database()
        db.create_db_dir()
        db.create_db()
        db_path = global_config['Database']['path']

        self.assertTrue(sqlite3.connect(db_path))
        self.assertTrue(DatabaseHandler().connect(db_path))
        self.assertTrue(DatabaseHandler().connect(None))
        #shutil.rmtree('honeyDB')


    def test_query_db(self):
        query_string = "SELECT * FROM test_http where port = 8082"
        json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
        for y in range(0, len(json_query) - 1):
            port_number = json_query[y].get('port')
            self.assertEqual(port_number, 8082)
        query_string = "SELECT * FROM test_http where port = 8083"
        json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
        self.assertEqual(json_query, [])
        query_string = "SELECT * FROM test_http where port = 8023"
        json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
        self.assertEqual(json_query, [])

        query_string = "SELECT * FROM test_http2 where port = 8083 AND eventDateTime = '1999-12-31T23:59:59'"
        json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
        self.assertEqual(len(json_query), 1)
        self.assertEqual(json_query[0].get('port'), 8083)
        self.assertEqual(json_query[0].get('eventDateTime'), '1999-12-31T23:59:59')

        query_string = "SELECT * FROM test_telnet where eventDateTime > '1999-12-31T23:59:59' " \
                       "AND eventDateTime < '2000-01-14T23:59:59'"
        json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
        self.assertEqual(len(json_query), 1)
        self.assertEqual(json_query[0].get('port'), 8023)
        self.assertEqual(json_query[0].get('eventDateTime'), '2000-01-07T23:59:59')

    def test_get_json_by_time(self):
        cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
        global_config = Configuration(cfg_path).getInstance()
        test_start_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
#        successes = 0
#        fails = 0
        for count in range (0, 2):
            if count == 0:
                portnumber = 8082
            elif count == 1:
                portnumber = 8083
            else:
                portnumber = 8023
            for x in range(0, 500):
                d = datetime.timedelta(weeks=x)
                query_date = (test_start_date + d)
                query_date_iso = query_date.isoformat()
                tableName = global_config.get_plugin_config(portnumber)['table']
                query_string = "SELECT * FROM %s where (eventDateTime >= '%s')" % (tableName, query_date_iso)
                json_query = DatabaseHandler().query_db(query_string, db="TestDB.sqlite")
                for y in range(0, len(json_query) - 1):
                    date = json_query[y].get('eventDateTime')
                    self.assertGreaterEqual(date, query_date_iso)
#                    if date >= query_date_iso:
#                        successes += 1
#                    else:
#                        fails += 1
#                with open("test_query_log.txt", "a") as log:
#                    log.write("Tested %s, had %d successes and %d fails\n" % (query_date_iso, successes, fails))
#                successes = 0
#                fails = 0

    def tearDown(self):
        os.remove("TestDB.sqlite")

if __name__ == "__main__":
    unittest.main()