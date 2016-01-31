import DB_Init
import Table_Init
import Table_Insert
import sqlite3
import unittest
import shutil

class table_insert_test_case(unittest.TestCase):
    def setUp(self):
        table_cols = []
        table_cols.append([1,'FRUIT','TEXT'])
        table_cols.append([2,'QTY','INTEGER'])
        table_cols.append([3,'COLOR','TEXT'])
        table = 'TEST1'
        DB_Init.create_default_database()
        Table_Init.create_table(table)
        Table_Init.add_columns(table,table_cols)

    def test_insert_data(self):
        table = 'TEST1'
        data = []
        data.append('Apple')
        data.append(10)
        data.append('Green')
        data2 = []
        data2.append('Banana')
        data2.append(5)
        data2.append('Yellow')
        Table_Insert.insert_data(table,data)
        Table_Insert.insert_data(table,data2)
        connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
        cursor = connection.cursor()
        result = cursor.execute('select * from TEST1 where ID = 1').fetchall()[0]
        result2 = cursor.execute('select * from TEST1 where ID = 2').fetchall()[0]
        result_check = (1,'Apple',10,'Green')
        result2_check = (2,'Banana',5,'Yellow')
        self.assertEquals(result,result_check)
        self.assertEquals(result2,result2_check)

    def tearDown(self):
        shutil.rmtree('./honeyDB')





