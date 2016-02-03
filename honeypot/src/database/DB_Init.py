import sqlite3
import os

'''use to create a folder and sqlite data file'''

def create_default_database():
    #if database directory does not exist create it
    if os.path.isdir('./honeyDB') == False:
        os.mkdir('./honeyDB')
    #if database file does not exist in directory create it
    if os.path.exists('./honeyDB/honeyDB.sqlite') == False:
        connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
        connection.close()




