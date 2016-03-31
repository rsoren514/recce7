################################################################################
#                                                                              #
#                           GNU Public License v3.0                            #
#                                                                              #
################################################################################
#   HunnyPotR is a honeypot designed to be a one click installable,            #
#   open source honey-pot that any developer or administrator would be able    #
#   to write custom plugins for based on specific needs.                       #
#   Copyright (C) 2016 RECCE7                                                  #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See their            #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public licenses         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
################################################################################

# SQLite to JSON code provided by StackOverflow user: Unmounted
# http://stackoverflow.com/users/11596/unmounted
# in an answer to the question "return SQL table as JSON in python"
# http://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
# Unmounted's code has been tailored for this project's purpose.

'''
This class will take in a request from the webserver, query the Sqlite database,
and return JSON.
Author: Charlie Mitchell
Last Revised: 30 March, 2016
'''

import os
import sqlite3

from common.GlobalConfig import Configuration
from reportserver.manager import dateTimeUtility

cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
global_config = Configuration(cfg_path).getInstance()
db_path = global_config.get_db_dir() + '/honeyDB.sqlite'

# Connect to given database.
# Defaults to the honeypot db, but another path can be passed in (mainly for testing)
def connect(database_name=db_path):
    return sqlite3.connect(database_name)

# Query DB and return JSON
# setting DB to TestDB created from DatabaseHandlerTest.py
def query_db(query, args=(), one=False):
    cur = connect().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

# Unit of Measure could be "weeks", "days", "hours", etc.
# Return all data from the DB within that measure of time as JSON.
def getJson(portnumber, unit, unit_size):

    # In progress... still need to test converting the timestamp received from the DB.
    begin_date = dateTimeUtility.get_begin_date(unit, unit_size)
    begin_date_iso = dateTimeUtility.get_iso_format(begin_date)
    tableName = getTableName(portnumber)
    date_time_field = getTableDateTimeField(portnumber)

    #  query = query_db("SELECT * FROM %s where (datetime > '%s')" % (tableName, query_date_iso))
    queryString = "SELECT * FROM %s where (%s > '%s')" % (tableName, date_time_field, begin_date_iso)
    print("queryString is: " + queryString)
    results = query_db(queryString)

    return results

def getTableName(portnumber):
    gc_dict = global_config.get_plugin_config(portnumber)
    return gc_dict['table']

def getTableDateTimeField(portnumber):
    return "eventDateTime"