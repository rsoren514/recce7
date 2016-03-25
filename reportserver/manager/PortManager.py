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

from reportserver.dao import DatabaseHandler


class PortManager:

    #TODO:
    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    #  Mgr for reading config files to know what table /column names there are.
    #  Utility for calc time range
    #
    #
    validPortNumbers = ()

    def __init__(self):
        # TODO:  get from config file
        self.validPortNumbers = (8023, 8082, 8083)


    def isPortValid(self, port_number):
        if (port_number in self.validPortNumbers):
            return True
        else:
            return False

    def getPort(self, port_number, uom, unit):
        print("Retrieving port:" + str(port_number))

        if self.isPortValid(port_number):
            return DatabaseHandler.getJson(port_number, uom, unit)
        else:
            return None


