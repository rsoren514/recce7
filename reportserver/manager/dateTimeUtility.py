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

'''
This class will handle any date/time requests from the webserver.
This includes calculating the date/time range for data to return,
as well as converting the string timestamp in the database.

Author: Charlie Mitchell
Last Revised: 28 February, 2016
'''

import datetime

from reportserver.manager import UnitOfMeasure


# Return the date for how far back to query DB.
def get_begin_date(unit, unit_size):
    if unit == UnitOfMeasure.MINUTE.value:
        d = datetime.timedelta(minutes=unit_size)
    elif unit == UnitOfMeasure.HOUR.value:
        d = datetime.timedelta(hours=unit_size)
    elif unit == UnitOfMeasure.DAY.value:
        d = datetime.timedelta(days=unit_size)
    elif unit == UnitOfMeasure.WEEK.value:
        d = datetime.timedelta(weeks=unit_size)
    else:
        d=1;  #defaults to 1 day but should never happen

    return calc_date(d)

def calc_date(delta):
    now = datetime.datetime.now()
    return now - delta

# Takes the datetime object and returns a string in ISO 8601 format.
def get_iso_format(begin_date):
    return begin_date.isoformat()