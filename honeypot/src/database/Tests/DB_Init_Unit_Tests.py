import shutil
import os
import unittest
from honeypot.src.database import DB_Init

#unit tests

'''This tests that the database directory is created'''


class DirectoryCreationTestCase(unittest.TestCase):
    #setup test case, run function to create directory
    def setUp(self):
        DB_Init.create_default_database()
    #test that the directory exists
    def test_directory_exists(self):
        self.assertTrue(os.path.isdir(DB_Init.get_home_dir() + DB_Init.get_home_config_path()))
    #remove the directory even though not empty
    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())

'''This test tests that the database file is created and exists'''


class DBFileCreationTestCase(unittest.TestCase):
    #setup test case, run function to create file
    def setUp(self):
        DB_Init.create_default_database()
    #test that the file exists
    def test_file_exists(self):
        self.assertTrue(os.path.exists(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                       DB_Init.get_database_config_name()))
    #remove the directory even though not empty
    def tearDown(self):
        shutil.rmtree(DB_Init.get_home_dir() + DB_Init.get_home_config_path())
