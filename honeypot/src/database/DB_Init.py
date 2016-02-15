import sqlite3
import os

'''use to create a folder and sqlite data file in the users home directory'''


def create_default_database():
    """if database directory does not exist create it"""
    if not os.path.isdir(get_home_dir() + get_home_config_path()):
        os.mkdir(get_home_dir() + get_home_config_path())
    '''if database file does not exist in directory create it'''
    if not os.path.exists(get_home_dir() + get_home_config_path() + '/' + get_database_config_name()):
        connection = sqlite3.connect(get_home_dir() + get_home_config_path() + '/' + get_database_config_name())
        connection.close()


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




