__author__ = 'Ben Phillips'
#this file will validate data and provide functionality to sort data by the columns defined in the database
#from honeypot.src.database import DB_Init
#from honeypot.src.database.config_temp import TempConfigObject
import sqlite3
from copy import deepcopy
from database import Table_Init


class DataValidation:

    #we should check the following

    #check dictionary length is 1 (done)
        #is the value a dictionary (done)
            #is the 1st value in the dictionary a string (done)
                #is the string a valid table name (done)
            #is the second value in the dictionary a dictionary (done)
                #are all the keys in the dictionary strings (done)
                    #are all the key strings in the dictionary found as column names in the database config for the table specified (done)
                    #are all the values in the dictionary correct python data types that are representative of their sqlite counterpart
    #table_schema = {}
    #tables = []
    def __init__(self,global_config_instance):
        #co = TempConfigObject.TempConfigObject()
        #ASK
        #I need a way to get the entire config so i can scan for all tables defined
        #table = co.get_config(8082).get('table')
        self.table_schema = {}
        self.tables = []
        connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
        cursor = connection.cursor()
        #will want to loop here through all tables found and store each schema
        #as an element in a list, this will require code changes throughout this file
        rows = cursor.execute("select name from sqlite_master where type = 'table';").fetchall()
        #transform list of tuples to a list of strings
        for row in rows:
            self.tables.append(row[0])
        for table in self.tables:
            table_def = cursor.execute('PRAGMA table_info(' + table + ');').fetchall()
            self.table_schema[table] = table_def
        cursor.close()

    #for updating tables and table schema class variables
    def update_tables_and_schema(self,global_config_instance):
        self.table_schema.clear()
        del self.tables[:]
        connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
        cursor = connection.cursor()
        #will want to loop here through all tables found and store each schema
        #as an element in a list, this will require code changes throughout this file
        rows = cursor.execute("select name from sqlite_master where type = 'table';").fetchall()
        #transform list of tuples to a list of strings
        for row in rows:
            self.tables.append(row[0])
        for table in self.tables:
            table_def = cursor.execute('PRAGMA table_info(' + table + ');').fetchall()
            self.table_schema[table] = table_def
        cursor.close()




    #return the class level variable tables
    def get_tables(self):
        return self.tables

    #return the class level variable table_schema
    def get_schema(self):
        return self.table_schema

    #checks the value length of the dictionary to make sure there is only one element
    @staticmethod
    def check_value_len(value):
        if len(value) == 1:
            return True
        else:
            return False

    #checks that the value is actually a dictionary
    @staticmethod
    def check_value_is_dict(value):
        if isinstance(value, dict):
            return True
        else:
            return False

    #checks that the key in the dictionary is a string
    @staticmethod
    def check_key_in_dict_string(value):
        if isinstance(DataValidation.get_first_key_value_of_dictionary(value), str):
            return True
        else:
            return False

    #checks that the key in the dictionary is a real table name in the database
    def check_key_is_valid_table_name(self,value):
        table_name = DataValidation.get_first_key_value_of_dictionary(value)
        if table_name in self.tables:
            return True
        else:
            return False

    #checks that the row data is actually a dictionary
    def check_row_value_is_dict(self,value):
        key = self.get_first_key_value_of_dictionary(value)
        if isinstance(value.get(key),dict):
            return True
        else:
            return False

    #gets the first key value in a dictionary
    @staticmethod
    def get_first_key_value_of_dictionary(value):
        return next(iter(value.keys()))

    #checks that all of the keys in the row data are strings
    def check_all_col_names_strings(self,value):
        key = self.get_first_key_value_of_dictionary(value)
        dict = value.get(key)
        count = len(dict.keys())
        compare = 0
        for key in dict.keys():
            if isinstance(key,str):
                compare += 1
        if count == compare:
            return True
        else:
            return False

    #this is WRONG need to fix, we need to verify that all plugin provided
    #columns exist in the database, not that all the database columns are
    #are provided by the plugin!
    #checks that all of the columns in the input exist in the target table, we do not check for ID
    def check_all_col_exist(self,value):
        key = self.get_first_key_value_of_dictionary(value)
        schema = self.table_schema[key]
        schema_col_list = [row[1] for row in schema]
        #remove ID because we do not require the plugin author to provide this
        schema_col_list = DataValidation.remove_default_columns_from_list([row[1] for row in schema])
        #get a list of column names from the table referenced in value
        prep_list = DataValidation.remove_default_columns_from_list(value[key])
        count = 0
        col_list = list(prep_list.keys())
        for col in col_list:
            if col in schema_col_list:
                count += 1

        #if (count == len(schema_col_list) and
        if (count == len(col_list)):
            return True
        else:
            return False

    @staticmethod
    def remove_default_columns_from_list(collection):
        collection_copy = deepcopy(collection)
        if isinstance(collection_copy,list):
            for col in Table_Init.default_columns:

                if col[0] in collection_copy:
                    collection_copy.remove(col[0])
            return collection_copy
        if isinstance(collection_copy,dict):
            for col in Table_Init.default_columns:
                if col[0] in collection_copy:
                    del collection_copy[col[0]]
            return collection_copy

    #TODO determine how to do this with regex
    def check_data_types(self,value):
        return True

    def run_all_checks(self, value):
        if (DataValidation.check_value_len(value) and
                DataValidation.check_value_is_dict(value) and
                DataValidation.check_key_in_dict_string(value) and
                self.check_key_is_valid_table_name(value) and
                self.check_all_col_names_strings(value) and
                self.check_all_col_exist(value) and
                self.check_data_types(value)):
            return True
        else:
            return False










