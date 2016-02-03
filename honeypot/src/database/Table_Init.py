import DB_Init
import sqlite3
import re
from operator import itemgetter

#DB_Init.create_default_database()



def create_table(name):
    connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE ' + name + '(ID INTEGER PRIMARY KEY)')
    connection.close()

def add_columns(name,column_list):
    verify_datatypes(column_list)
    connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
    cursor = connection.cursor()
    column_list_sorted = sorted(column_list , key=itemgetter(0))
    for x in column_list_sorted:
        cursor.execute('ALTER TABLE ' + name + ' ADD COLUMN ' + x[1] + ' ' + x[2])
    connection.close()

def verify_datatypes(column_list):
    valid_datatypes = ('NULL','INTEGER','REAL','TEXT','BLOB')
    for row in column_list:
        if row[2] in valid_datatypes:
            pass
        else:
            raise ValueError('Verifying ' + str(row) + ' : ' + row[2] +
                             ' is not a valid SQLITE3 datatype')



