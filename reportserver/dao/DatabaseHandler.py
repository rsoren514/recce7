__author__ = 'Charlie Mitchell <belmontrevenge@gmail.com>'
'''
This class will take in a request from the webserver, query the Sqlite database,
and return JSON.
'''

import os
import sqlite3

from common.globalconfig import GlobalConfig
from reportserver.manager import dateTimeUtility

plugin_cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
global_cfg_path = os.getenv('RECCE7_GLOBAL_CONFIG') or 'config/global.cfg'
global_config = GlobalConfig(plugin_cfg_path, global_cfg_path)
global_config.read_global_config()
global_config.read_plugin_config()
db_path = global_config['Database']['path']

# Connect to given database.
# Defaults to the honeypot db, but another path can be passed in (mainly for testing).
# Database needs to exist first.
def connect(database_name=db_path):
    if not os.path.exists(database_name):
        print("Database does not exist in path: " + database_name)
        return None
    try:
        conn = sqlite3.connect(database_name)
    except sqlite3.OperationalError:
        print("Error connecting to database at: " + database_name)
    else:
        return conn

# Query DB and return JSON
# setting DB to TestDB created from DatabaseHandlerTest.py
def query_db(query, args=(), one=False, db=db_path):
    #print ("args are: " +str(args))
    cur = connect(db).cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

# Unit of Measure could be "weeks", "days", "hours", "minutes".
# Return all data from the DB within that measure of time as JSON.
def get_json_by_time(portnumber, uom, units):
    begin_date_iso = get_begin_date_iso(uom, units)
    tableName = global_config.get_plugin_config(portnumber)['table']
    date_time_field = global_config['Database']['datetime.name']

    #  query = query_db("SELECT * FROM %s where (datetime > '%s')" % (tableName, query_date_iso))
    queryString = "SELECT * FROM %s where %s >= '%s'" % (tableName, date_time_field, begin_date_iso)
    #args = (tableName, date_time_field, begin_date_iso)
    print("queryString is: " + str(queryString))
    #print ("args to use: " + str(args))
    results = query_db(queryString)
    # print("results: " + results)

    return results

def get_begin_date_iso(uom, units):
    begin_date = dateTimeUtility.get_begin_date(uom, units)
    begin_date_iso = dateTimeUtility.get_iso_format(begin_date)
    return begin_date_iso


