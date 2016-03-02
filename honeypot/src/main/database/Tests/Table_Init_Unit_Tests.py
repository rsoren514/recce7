import unittest
import sqlite3
from database import Table_Init
import shutil
from database import DB_Init

#unit tests

'''This test verifies that the create_table method actually creates a table'''


class TableCreationTestCase(unittest.TestCase):

    def test_create_table(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')
        connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                     DB_Init.get_database_config_name())
        cursor = connection.cursor()
        table_list = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[0]
        self.assertIn('TestTable1', table_list)
        connection.close()

    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())

'''This test checks that the add_columns function indeed adds columns to the database
   table provided and also that they are in the correct order'''


class TableColumnAddTestCase(unittest.TestCase):

    def setUp(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')

    def test_add_columns(self):
        col_list = [[1, 'Fruit', 'TEXT'], [2, 'Quantity', 'INTEGER'], [3, 'Color', 'TEXT']]
        Table_Init.add_columns('TestTable1', col_list)
        connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                     DB_Init.get_database_config_name())
        cursor = connection.cursor()
        column_data = cursor.execute("PRAGMA table_info(TestTable1)").fetchall()
        connection.close()
        column_list = []
        for record in column_data:
            column_list.append(record[1])
        self.assertEquals(column_list[0], 'ID')
        self.assertEquals(column_list[1], 'Fruit')
        self.assertEquals(column_list[2], 'Quantity')
        self.assertEquals(column_list[3], 'Color')

    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())

'''This test checks that even when the list items are provided out of order the add_columns
   function still adds them in the order prescribed by the order column in the list'''


class TableColumnAddOrderTestCase(unittest.TestCase):

    def setUp(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')

    def test_add_columns(self):
        col_list = [[3, 'Color', 'TEXT'], [1, 'Fruit', 'TEXT'], [2, 'Quantity', 'INTEGER']]
        Table_Init.add_columns('TestTable1', col_list)
        connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                     DB_Init.get_database_config_name())
        cursor = connection.cursor()
        column_data = cursor.execute("PRAGMA table_info(TestTable1)").fetchall()
        connection.close()
        column_list = []
        for record in column_data:
            column_list.append(record[1])
        self.assertEquals(column_list[0], 'ID')
        self.assertEquals(column_list[1], 'Fruit')
        self.assertEquals(column_list[2], 'Quantity')
        self.assertEquals(column_list[3], 'Color')

    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())

'''This test checks that attempts to add columns with invalid data types results in an error'''


class TableColumnVerifyDataTypeTestCase(unittest.TestCase):

    def test_verify_data_types(self):
        test_list = [[1, 'FRUIT', 'TEXT'], [2, 'QUANTITY', 'INTXGER'], [3, 'COLOR', 'TXET']]
        self.assertRaises(ValueError, Table_Init.verify_data_types, test_list)

'''this test checks that the method that checks to see if a table exists works correctly
   also verifies that it is case sensitive'''
class TableCheckExistsTestCase(unittest.TestCase):
    def setUp(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')
        Table_Init.create_table('TESTTABLE2')

    def test_check_table_exists(self):
        self.assertTrue(Table_Init.check_table_exists('TestTable1'))
        self.assertTrue(Table_Init.check_table_exists('TESTTABLE2'))
        self.assertFalse(Table_Init.check_table_exists('TESTTABLE1'))
        self.assertFalse(Table_Init.check_table_exists('TestTable2'))

    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())
