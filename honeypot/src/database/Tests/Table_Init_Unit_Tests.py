import unittest
import sqlite3
import Table_Init
import shutil
import DB_Init

class table_creation_test_case(unittest.TestCase):


    def test_create_table(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')
        connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
        cursor = connection.cursor()
        table_list = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[0]
        self.assertIn('TestTable1',table_list)
        connection.close()

    def tearDown(self):
        shutil.rmtree('./honeyDB')

class table_column_add_test_case(unittest.TestCase):

    def setUp(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')

    def test_add_columns(self):
        col_list = []
        col_list.append([1,'Fruit','TEXT'])
        col_list.append([2,'Quantity','INTEGER'])
        col_list.append([3,'Color','TEXT'])
        Table_Init.add_columns('TestTable1',col_list)
        connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
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
        shutil.rmtree('./honeyDB')

class table_column_add_order_test_case(unittest.TestCase):

    def setUp(self):
        DB_Init.create_default_database()
        Table_Init.create_table('TestTable1')

    def test_add_columns(self):
        col_list = []
        col_list.append([3,'Color','TEXT'])
        col_list.append([1,'Fruit','TEXT'])
        col_list.append([2,'Quantity','INTEGER'])
        Table_Init.add_columns('TestTable1',col_list)
        connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
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
        shutil.rmtree('./honeyDB')

class table_column_verify_datatype_test_case(unittest.TestCase):

    def test_verify_datatypes(self):
        test_list = []
        test_list.append([1,'FRUIT','TEXT'])
        test_list.append([2,'QUANTITY','INTXGER'])
        test_list.append([3,'COLOR','TXET'])
        self.assertRaises(ValueError,Table_Init.verify_datatypes,test_list)



