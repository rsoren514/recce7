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
Last Revised: 4 March, 2016
'''

import os
import sqlite3

from reportserver.manager import dateTimeUtility


# Connect to given database
def connect(database_name):
    return sqlite3.connect(database_name)

# Query DB and return JSON
# setting DB to TestDB created from GetJSONUnitTests.py
def query_db(query, args=(), one=False):
    cur = connect(get_db_path()).cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

# For now, assume outside request specifies Port Number, Unit of Measure (string), and Unit Size.
# Where Unit of Measure could be "weeks", "days", "hours", etc.
# Return all data from the DB within that measure of time as JSON.
#
# I'm assuming here that the DB's timestamp will use datetime.now().

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


#####
### this section below will be in the global config py once we decide how we want to share it
####
def getTableName(portnumber):
    #  TODO:  call something to determine this name
    if portnumber == 8023:
        return "test_telnet"
    elif portnumber == 8082:
        return "test_http"
    else:
        return "test_http2"


def get_db_path():
        #
        # TODO: use global config for this
        return os.getenv('HOME') + '/honeyDB/honeyDB.sqlite'

def getTableDateTimeField(portnumber):
    return "eventdatetime"