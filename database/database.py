import ntpath
import os
import sqlite3
from database import Table_Init
from database.DataValidation import DataValidation
from common.logger import Logger

__author__ = 'Ben Phillips'


class Database:
    def __init__(self, global_config):
        self.global_config = global_config
        self.log = Logger().get('database.database.Database')
        
    def create_default_database(self):
        """
        Calls methods needed to create the database.
        """
        self.create_db_dir()
        self.create_db()
        Table_Init.run_db_scripts(self.global_config)
        self.update_schema()
    
    def create_db_dir(self):
        """
        Creates the database directory if it doesn't already exist.
        """

        # if database directory does not exist create it
        db_path = self.global_config['Database']['path']
        (db_dir, db_name) = ntpath.split(db_path)
        if not os.path.isdir(db_dir):
            self.log.info("Database directory not found, "
                          "creating database directory...")
            os.mkdir(db_dir)
    
    def create_db(self):
        """
        Creates the database if it doesn't already exist.
        """

        # if database file does not exist in the directory, create it
        (db_dir, db_name) = ntpath.split(self.global_config['Database']['path'])
        if not os.path.exists(self.global_config['Database']['path']):
            self.log.info("Database file not found, creating database file...")

            # this actually creates the database file
            connection = sqlite3.connect(self.global_config['Database']['path'])
            connection.close()
    
    def update_schema(self):
        """
        Migrates the database when columns have been added or
        removed to the schema.
        """

        #
        # holds the list of tables defined in the configuration
        # if the distinct sets of tables are not equal
        # create database tables that do not exist
        #
        self.create_non_exist_tables(
            self.table_list_diff(
                #RANDY this may be unnecessary coupling or a good reason
                #to absorb DataValidation into DB_Init.
                DataValidation(self.global_config).get_tables(),
                self.get_config_table_list(
                    self.global_config.get_ports(),
                    self.global_config.get_plugin_dictionary())))

        # now that the tables do exist lets update the information from the
        # database
        DataValidation(self.global_config).update_tables_and_schema(self.global_config)
        # now our tables exist with a primary key sequence of ID
        # now i must check each table and add columns
        # create a dictionary of config column lists
        # create a dictionary of database column lists
        #

        # transform database column list this contains the column definitions
        # in the same way as the config does'''
        self.update_table_structure()

    def get_config_table_list(self, port_list, schema_dict):
        """
        returns the table list from the configuration singleton that
        correspond to ports provided
        """
        config_table_list = []
        for port in port_list:
            config = schema_dict.get(port)
            config_table_list.append(config.get('table'))
        return config_table_list

    def table_list_diff(self, current_database_table_list, config_table_list):
        """
        return list of tables that are different between the current database
         table list and the config's table list
        """
        if not set(current_database_table_list) == set(config_table_list):
            # return the left hand difference between the schema and config
            # table sets
            return list(set(config_table_list) - set(current_database_table_list))
        else:
            return []

    def create_non_exist_tables(self, table_diff):
        """
        create tables that do not exist from the table difference between the current database and the configuration
        """
        if len(table_diff) > 0:
            for table in table_diff:
                Table_Init.create_table(table, self.global_config)
            self.log.info('Updated database schema, table names now match configuration.')
        else:
            self.log.info('Database Schema and Configuration table names already match.')
    
    def create_dict_config_column_list(self):
        """
        get a dictionary of tables and corresponding columns from the config
        """
        config_column_lists = {}
        for port in self.global_config.get_ports():
            value = self.global_config.get_plugin_dictionary().get(port)
            config_column_lists[value.get('table')] = value.get('tableColumns')
        return config_column_lists
    
    def create_dict_schema_column_list(self):
        """
        get a dictionary of tables and corresponding columns from the existing
        database
        """
        database_column_lists = {}
        database_schema = DataValidation(self.global_config).get_schema()
        for schema in database_schema:
            database_column_lists[schema] = database_schema.get(schema)
        return database_column_lists
    
    def create_dict_transformed_column_list(self, database_column_lists):
        """
        returns only custom plugin defined columns from database schema i.e.
        ignores default columns
        """
        transformed_db_column_list = {}
        for table in database_column_lists:
            col_list = database_column_lists.get(table)
            for column in col_list:
                transformed_db_column_list[table] = []
            # default column ids to ignore
            default_list = []
            for default in Table_Init.default_columns:
                default_list.append(default[0])
            for column in col_list:
                # ignores the default columns
                if column[1] in default_list:
                    continue
                transformed_db_column_list[table].append([column[0],column[1],column[2]])
        return transformed_db_column_list
    
    def update_table_structure(self):
        for table in self.create_dict_config_column_list():
                if not [(x[1],x[2]) for x in self.create_dict_config_column_list().get(table)] == \
                       [(x[1],x[2]) for x in self.create_dict_transformed_column_list(self.create_dict_schema_column_list()).get(table)]:
                    Table_Init.change_table_structure(table,
                                                      self.create_dict_config_column_list().get(table),
                                                      self.create_dict_schema_column_list().get(table),
                                                      self.global_config)
