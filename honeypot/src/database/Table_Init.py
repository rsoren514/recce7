from honeypot.src.database import DB_Init
import sqlite3
from operator import itemgetter

'''DB_Init.create_default_database()'''

'''create a table in the sqlite database with the name of the table passed in'''


def create_table(name):
    connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                 DB_Init.get_database_config_name())
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE ' + name + '(ID INTEGER PRIMARY KEY)')
    connection.close()


'''add columns to the table, requires the name of the table and the column list
   this column list currently contains [column order],[column name],[column type]'''


def add_columns(name,column_list):
    verify_data_types(column_list)
    connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                 DB_Init.get_database_config_name())
    cursor = connection.cursor()
    column_list_sorted = sorted(column_list, key=itemgetter(0))
    for x in column_list_sorted:
        cursor.execute('ALTER TABLE ' + name + ' ADD COLUMN ' + x[1] + ' ' + x[2])
    connection.close()


'''check that the data types passed in are valid sqlite data types'''


def verify_data_types(column_list):
    valid_data_types = ('NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB')
    for row in column_list:
        if row[2] in valid_data_types:
            pass
        else:
            raise ValueError('Verifying ' + str(row) + ' : ' + row[2] +
                             ' is not a valid SQLITE3 data type')


'''check if table name exists, is case sensitive'''


def check_table_exists(name):
    connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                 DB_Init.get_database_config_name())
    cursor = connection.cursor()
    table_count = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='" + name + "';").fetchall()
    connection.close()
    if table_count[0][0] > 0:
        return True
    else:
        return False




