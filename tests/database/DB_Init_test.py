from database import DB_Init
from database import Table_Init
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
        gci = Configuration('tests/database/test.cfg').getInstance()
        DB_Init.create_db_dir(gci)
        self.assertFalse(os_mkdir.called)

    @patch('os.mkdir')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_non_exist)
    def test_create_db_dir_non_exist(self, gci_get_db_dir, os_mkdir):
        gci = Configuration('tests/database/test.cfg').getInstance()
        DB_Init.create_db_dir(gci)
        self.assertTrue(os_mkdir.called)

    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_create_db_database_exists(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration('tests/database/test.cfg').getInstance()
        DB_Init.create_db(gci)
        self.assertFalse(sqlite3_connect.called)

    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_exist)
    def test_create_db_database_non_exist(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration('tests/database/test.cfg').getInstance()
        DB_Init.create_db(gci)
        self.assertTrue(sqlite3_connect.called)

    def test_table_list_diff(self):
        table_list = ['table1', 'table2', 'table3']
        table_list_match = ['table2', 'table3', 'table1']
        table_list_non_match = ['table2', 'table3', 'table4']
        self.assertTrue(DB_Init.table_list_diff(table_list, table_list_non_match) == ['table4'])
        self.assertTrue(DB_Init.table_list_diff(table_list, table_list_match) == [])

    def test_get_config_table_list(self):
        expected_tables = ['test_http_test', 'test_http2_test', 'test_telnet_test']
        gci = Configuration('tests/database/test.cfg').getInstance()
        self.assertEqual(expected_tables, DB_Init.get_config_table_list(gci.get_ports(), gci.get_plugin_dictionary()))

    @patch('database.Table_Init.create_table')
    def test_create_non_exist_tables(self, Table_Init_mod):
        gci = Configuration('tests/database/test.cfg').getInstance()
        table_diff = ['test4']
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertTrue(Table_Init_mod.called)

    @patch('database.Table_Init.create_table')
    def test_count_create_non_exist_tables(self, Table_Init_mod):
        gci = Configuration('tests/database/test.cfg').getInstance()
        table_diff = ['test4', 'test5', 'test6']
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertEqual(3, Table_Init_mod.call_count)

    @patch('database.Table_Init.create_table')
    def test_create_non_exist_tables(self, Table_Init_mod):
        gci = Configuration('tests/database/test.cfg').getInstance()
        table_diff = []
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertFalse(Table_Init_mod.called)

    def test_create_dict_config_column(self):
        expected_column_list = {'test_telnet_test': [[1, 'Test_col', 'TEXT'], [2, 'User_Data', 'TEXT']],
                                'test_http2_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']],
                                'test_http_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']]}
        gci = Configuration('tests/database/test.cfg').getInstance()
        self.assertTrue(expected_column_list == DB_Init.create_dict_config_column_list(gci))

    def test_create_dict_config_column(self):
        expected_column_list = {'test_telnet_test_wrong': [[1, 'Test_col', 'TEXT'], [2, 'User_Data', 'TEXT']],
                                'test_http2_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']],
                                'test_http_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']]}
        gci = Configuration('tests/database/test.cfg').getInstance()
        self.assertFalse(expected_column_list == DB_Init.create_dict_config_column_list(gci))











