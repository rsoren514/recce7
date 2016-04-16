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

from reportserver.manager.UnitOfMeasure import UnitOfMeasure


#Given a string, try to convert it to an int.
def validate_port_number(givenStr):
    print("given str is: " + givenStr)
    try:
        return int(givenStr)
    except Exception as e:
        print("Received invalid string to convert to int: " + givenStr)
        print (str(e))
        return None


#Given a token
def validate_time_period(query_tokens):

    uom = None
    units = None

    print("given query_tokens:" + str(query_tokens))

    for token in query_tokens:
        uom,units = token.split('=')
        if uom in UnitOfMeasure.get_values(UnitOfMeasure):
            units = int(units)
            break
        else:
            uom  = None
            units = None

    print("\n validate_time_period:" + str(uom) + ": " + str(units))
    return (uom, units)

def get_path_query_tokens(path):
    path_query_tokens = path.split('?')
    query_tokens = []

    path_tokens = path_query_tokens[0].split('/')
    #print('path tokens: ', path_tokens)

    if len(path_query_tokens) > 1:
        query_tokens = path_query_tokens[1].split('&')
        #print('query tokens: ', query_tokens)


    return path_tokens, query_tokens
