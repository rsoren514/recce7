import shutil
import os
import unittest
import DB_Init

#unit tests
class directoryCreationTestCase(unittest.TestCase):
    #setup test case, run function to create directory
    def setUp(self):
        DB_Init.create_default_database()
    #test that the directory exists
    def test_directory_exists(self):
        self.assertTrue(os.path.isdir('./honeyDB'))
    #remove the directory even though not empty
    def tearDown(self):
        shutil.rmtree('./honeyDB')

class dbFileCreationTestCase(unittest.TestCase):
    #setup test case, run function to create file
    def setUp(self):
        DB_Init.create_default_database()
    #test that the file exists
    def test_file_exists(self):
        self.assertTrue(os.path.exists('./honeyDB/honeyDB.sqlite'))
    #remove the directory even though not empty
    def tearDown(self):
        shutil.rmtree('./honeyDB')
