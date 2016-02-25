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

import datetime
import json
import sqlite3
from server.UnitOfMeasure import UnitOfMeasure

class Getjson:

    ''' Set to hardcode the database. Still need to work on getting the database location
        from the config file. '''
    def db(database_name='Database Name'):
        return sqlite3.connect("DB.db")

    # Query DB and return JSON
    def query_db(query, args=(), one=False):
        cur = db().cursor()
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

    def getjson(portnumber, unit, unit_size):
        # In progress... still need to test converting the timestamp received from the DB.
        query_date = get_begin_date(unit, unit_size)

    # Return the date for how far back to query DB.
    def get_begin_date(unit, unit_size):
        if unit == UnitOfMeasure.MINUTE:
            d = timedelta(minutes=unit_size)
        elif unit == UnitOfMeasure.HOUR:
            d = timedelta(hours=unit_size)
        elif unit == UnitOfMeasure.DAY:
            d = timedelta(days=unit_size)
        elif unit == UnitOfMeasure.WEEK:
            d = timedelta(weeks=unit_size)
        else:
            return 0
        return calc_date(d)

    # Returns a new datetime with the current date minus the units specified.
    def calc_date(delta):
        now = datetime.datetime.now()
        return (now - delta)

#    json_output = json.dumps(my_query)
#    print(json_output)