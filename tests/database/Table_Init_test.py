import unittest
import sqlite3
from database import Table_Init
from database import DB_Init
from common.GlobalConfig import GlobalConfig
from common.GlobalConfig import Configuration
from unittest.mock import patch
import os
#unit tests

'''This test verifies that the create_table method actually creates a table'''
testpath = os.getcwd() + '/tests/database/Table_Init_testDir/honeyDB'

class TableCreationTestCase(unittest.TestCase):


    def setUp(self):
        self.gci = Configuration('tests/database/test_configs/Table_Init_test.cfg').getInstance()

    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath)
    def test_create_table(self,gci_get_db_dir):
        DB_Init.create_default_database(self.gci)
        Table_Init.create_table('TestTable1',self.gci)
        connection = sqlite3.connect(self.gci.get_db_dir() + '/honeyDB.sqlite')
        cursor = connection.cursor()
        table_list = []
        for table_tuple in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
            table_list.append(table_tuple[0])
        self.assertIn('TestTable1', table_list)
        connection.close()

    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath)
    def tearDown(self,gci_get_db_dir):
        os.remove(self.gci.get_db_dir() + '/honeyDB.sqlite')