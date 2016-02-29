#from honeypot.src.database import DB_Init
import sqlite3
from operator import itemgetter

'''DB_Init.create_default_database()'''

'''create a table in the sqlite database with the name of the table passed in'''


def create_table(name,global_config_instance):
    connection = sqlite3.connect(global_config_instance.get_db_path())
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE ' + name + '(ID INTEGER PRIMARY KEY)')
    connection.close()


'''add columns to the table, requires the name of the table and the column list
   this column list currently contains [column order],[column name],[column type]'''


def add_columns(name,column_list,global_config_instance):
    verify_data_types(column_list)
    connection = sqlite3.connect(global_config_instance.get_db_path())
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


def check_table_exists(name,global_config_instance):
    connection = sqlite3.connect(global_config_instance.get_db_path())
    cursor = connection.cursor()
    table_count = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='" + name + "';").fetchall()
    connection.close()
    if table_count[0][0] > 0:
        return True
    else:
        return False


'''change table structure'''

def change_table_structure(name,config_column_list,db_column_list,global_config_instance):
    '''rename old table'''
    connection = sqlite3.connect(global_config_instance.get_db_path())
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE " + name + " RENAME TO " + name + "_delme")
    '''create new table'''
    create_table(name,global_config_instance)
    '''copy old data to new table warning you may lose data if the
       columns arent there in the new table'''
    add_columns(name,config_column_list,global_config_instance)
    '''find columns in common between database and config'''
    #todo write code to copy data once we have code to create table data

    '''remove old table'''
    delete_table(name,global_config_instance)





'''deletes table'''
def delete_table(name,global_config_instance):
    connection = sqlite3.connect(global_config_instance.get_db_path())
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + name + "_delme;")
    cursor.close



