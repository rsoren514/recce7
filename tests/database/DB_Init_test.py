from database import DB_Init
from common.GlobalConfig import GlobalConfig
from common.GlobalConfig import Configuration
import unittest
from unittest import mock
from unittest.mock import patch
import os
import sqlite3

class DB_Init_test(unittest.TestCase):

    testpath_exist = os.getcwd() + '/tests/database/testDir'
    testpath_non_exist = os.getcwd() + '/tests/database/testDirDoesNotExist'
    testpath_with_db = os.getcwd() + '/tests/database/testDirDB'


    @patch('os.mkdir')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_exist)
    def test_create_db_dir_exists(self, gci_get_db_dir, os_mkdir):
        gci = Configuration().getInstance()
        DB_Init.create_db_dir(gci)
        self.assertFalse(os_mkdir.called)

    @patch('os.mkdir')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_non_exist)
    def test_create_db_dir_non_exist(self, gci_get_db_dir, os_mkdir):
        gci = Configuration().getInstance()
        DB_Init.create_db_dir(gci)
        self.assertTrue(os_mkdir.called)

    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_create_db_database_exists(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration().getInstance()
        DB_Init.create_db(gci)
        self.assertFalse(sqlite3_connect.called)

    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_exist)
    def test_create_db_database_non_exist(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration().getInstance()
        DB_Init.create_db(gci)
        self.assertTrue(sqlite3_connect.called)


class DB_Init_Get_Config_test(unittest.TestCase):

    def test_get_config_table_list(self):
        expected_tables = ['test_http_test', 'test_http2_test', 'test_telnet_test']
        gci = Configuration('tests/database/test.cfg').getInstance()
        list = DB_Init.get_config_table_list(gci.get_ports(), gci.get_plugin_dictionary())
        self.assertEqual(expected_tables, list)










