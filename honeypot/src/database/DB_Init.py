import sqlite3
import os
from honeypot.src.database import Table_Init
from honeypot.src.database.DataValidation import DataValidation
'''use to create a folder and sqlite data file in the users home directory'''


def create_default_database(global_config_instance):
    """if database directory does not exist create it"""
    if not os.path.isdir(global_config_instance.get_db_dir()):
        os.mkdir(global_config_instance.get_db_dir())
    '''if database file does not exist in directory create it'''
    if not os.path.exists(global_config_instance.get_db_path()):
        connection = sqlite3.connect(global_config_instance.get_db_path())
        connection.close()
    '''now the database is guaranteed to exist, we must find out if the
       schema is correct and create the appropriate tables I am creating
       another validation object for this purpose and am also storing the
       schema and port list locally so that it is easy to do this'''
    dv = DataValidation(global_config_instance)
    schema_dict = global_config_instance.config_dictionary
    port_list = global_config_instance.enabled_ports
    #print(schema_dict)
    current_database_table_list = dv.get_tables()
    '''holds the list of tables defined in the configuration'''
    config_table_list = []
    for port in port_list:
        config = schema_dict.get(port)
        config_table_list.append(config.get('table'))
    '''if the distinct sets of tables are not equal'''
    table_diff = []
    if not set(current_database_table_list) == set(config_table_list):
        '''lets get the difference of the sets so that we can add new tables'''
        '''from what i can tell this is the left hand difference meaning that
           it will only show us what is in the config that isnt in the database
           already'''
        #print(current_database_table_list)
        table_diff = list(set(config_table_list) - set(current_database_table_list))

    '''create database tables that do not exist'''
    if len(table_diff) > 0:
        for table in table_diff:
            Table_Init.create_table(table,global_config_instance)
    '''now that the tables do exist lets update the information from the database'''
    dv.update_tables_and_schema(global_config_instance)


    '''now our tables exist with a primary key sequence of ID'''
    '''now i must check each table and add columns'''
    '''create a dictionary of config column lists'''

    config_column_lists = {}
    for port in port_list:
        value = schema_dict.get(port)
        config_column_lists[value.get('table')] = value.get('tableColumns')
    '''create a dictionary of database column lists'''
    database_column_lists = {}
    database_schema = dv.get_schema()
    for schema in database_schema:
        database_column_lists[schema] = database_schema.get(schema)
    #print(config_column_lists)
    #print(database_column_lists)
    '''transform database column list this contains the column definitions in
       the same way as the config does'''
    transformed_db_column_list = {}
    for table in database_column_lists:
        col_list = database_column_lists.get(table)
        for column in col_list:
            transformed_db_column_list[table] = []
        for column in col_list:
            '''ignores the ID columns'''
            if column[1] == 'ID':
                continue
            transformed_db_column_list[table].append([column[0],column[1],column[2]])

    for table in config_column_lists:
        print('config_column_lists: ' + str(config_column_lists))
        print('transoformed_db_column_lists: ' + str(transformed_db_column_list))
        if not config_column_lists.get(table) == transformed_db_column_list.get(table):
            Table_Init.change_table_structure(table,config_column_lists.get(table),database_column_lists.get(table),global_config_instance)

    '''create a list of columns to add per table'''
    #print(transformed_db_column_list)
    #Table_Init.change_table_structure('test4',None,global_config_instance)
    #for port in port_list:

'''these functions are stubbed at the moment we will want to link them to the
   configuration utility once that is up and running'''


def get_database_config_name():
    return 'honeyDB.sqlite'


def get_home_config_path():
    return '/honeyDB'


'''this returns the users HOME environment variable which we can use to decide
   where to put the database, i believe we decided it can live in the users home
   directory but the name of the file and the directory within home can be
   configured in the config'''


def get_home_dir():
    return os.getenv('HOME')





#todo


