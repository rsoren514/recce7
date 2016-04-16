__author__ = 'Ben Phillips'

#from honeypot.src.database import DB_Init
import sqlite3
from operator import itemgetter
import os

'''DB_Init.create_default_database()'''

'''create a table in the sqlite database with the name of the table passed in'''

'''this list contains the default columns that the base plugin will control'''
'''this is useful because when we are verifying that all of the columns provided
by the custom plugin are indeed in the database we can ignore these programatically
as they are not controlled by the author'''
default_columns = [['ID','INTEGER','PRIMARY KEY', 'NOT NULL'],
                   ['session','TEXT','','NULL'],
                   ['eventDateTime','TEXT','','NULL'],
                   ['peerAddress','TEXT','','NULL'],
                   ['localAddress','TEXT','','NULL']]

def create_table(name,global_config_instance):
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
    cursor = connection.cursor()

    default_column_def = ''
    count = 0
    for col in default_columns:
        count += 1
        default_column_def += col[0] + ' ' + col[1] + ' ' + col[2] + ' ' + col[3]
        if count != len(default_columns):
            default_column_def += ','
    default_column_def = default_column_def.replace('  ',' ')

    #cursor.execute('CREATE TABLE ' + name + '(ID INTEGER PRIMARY KEY, eventDateTime TEXT NULL, '
    #                                        'peerAddress TEXT NULL, localAddress Text NULL)')
    cursor.execute('CREATE TABLE ' + name + '(' + default_column_def + ')')
    connection.close()

'''this method will run all db scripts in the scripts directory to create non-user defined sqlite objects'''
def run_db_scripts(global_config_instance):
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
    cursor = connection.cursor()
    script_path = '/database/sql_scripts'
    file_list = os.listdir(os.getcwd() + script_path)
    for file in file_list:
        open_file = open(os.getcwd() + script_path + '/' + file,'r')
        cursor.execute(open_file.read())
        open_file.close()
    connection.close()



'''add columns to the table, requires the name of the table and the column list
   this column list currently contains [column order],[column name],[column type]'''


def add_columns(name,column_list,global_config_instance):
    verify_data_types(column_list)
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
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
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
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
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
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
    connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
    cursor = connection.cursor()
    '''if you are deleting a table due to changing the configuration of the columns lets remove any sessions from the
       sessions table referencing the old table'''
    if(cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='" + name + "_delme';").fetchall()[0][0] > 0):
        cursor.execute("DELETE from sessions where table_name = '" + name + "';")
    cursor.execute("DROP TABLE IF EXISTS " + name + "_delme;")
    cursor.close



