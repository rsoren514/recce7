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
from common.GlobalConfig import Configuration
from reportserver.dao import DatabaseHandler
from reportserver.manager import dateTimeUtility

import dateutil.parser


class PortManager:

    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    # List of valid ports it can receive is taken from the Configuration setup.
    #
    #
    validPortNumbers = ()

    def __init__(self):
        self.g_config = Configuration().getInstance()
        self.validPortNumbers = self.g_config.get_ports()
        self.date_time_field = self.g_config.get_db_datetime_name()


    def isPortValid(self, port_number):
        if (port_number in self.validPortNumbers):
            return True
        else:
            return False

    def getPort(self, port_number, uom, unit):
        print("#info Retrieving port:" + str(port_number) + "uom:" + uom + " size: " + str(unit))

        if self.isPortValid(port_number):
            results = DatabaseHandler.get_json_by_time(port_number, uom, unit)
            if (results == None):
                return results
            else:
                return self.process_port_data(results)
        else:
            return None


    def get_port_attack_count(self, tablename, unit, uom):
        fromDate = dateTimeUtility.get_begin_date_iso(unit, uom)

        sql = "select count(distinct session) as total_attacks from %s where %s >= '%s' " %(tablename, self.date_time_field, fromDate)
        print("#debug sql is:" + sql)
        result = DatabaseHandler.query_db(sql)[0]
        return int(result['total_attacks'])

    def get_unique_ips(self, tablename, unit, uom):
        fromDate = dateTimeUtility.get_begin_date_iso(unit, uom)
        sql = "select count(distinct localAddress) as unique_ips from %s where %s >= '%s' " % (tablename, self.date_time_field, fromDate)
        print("#debug sql is:" + sql)
        result = DatabaseHandler.query_db(sql)[0]
        return int(result['unique_ips'])


    def process_port_data(self, results):
        first_row = results[0]
        current_session = first_row['session']

        port_data_json = []

        session_json = self.setup_session_json(first_row)

        session_rows= []

        for row in results:
            #handle session changes
            if (row['session'] != current_session):
                session_json['session_items'] = session_rows.copy()
                session_json['duration']=  self.get_date_delta(session_json['begin_time'],session_json['end_time'])
                port_data_json.append(session_json)
                session_rows.clear()
                current_session = row['session']
                session_json = self.setup_session_json(row)
            #append each row
            session_rows.append(row)
            session_json['end_time'] = row['eventDateTime']

        #handle the end of rows here
        session_json['session_items'] = session_rows.copy()
        session_json['duration'] = self.get_date_delta(session_json['begin_time'],session_json['end_time'])
        port_data_json.append(session_json)

        return port_data_json


    def setup_session_json(self, row):
        session_json = {
            'session': row['session'],
            'begin_time': row['eventDateTime'],
            'end_time': row['eventDateTime'],
            'local_address': row['localAddress'],
            'peer_address': row['peerAddress']
        }
        return session_json

    def get_date_delta(self,iso_date_from, iso_date_to):

        try:
            date_from = dateutil.parser.parse(iso_date_from)
            date_to = dateutil.parser.parse(iso_date_to)
            delta = date_to - date_from
        except Exception as e:
            print("Error: "+ e.message)
            delta = 0

        return str(delta)