
from common.GlobalConfig import Configuration
from reportserver.dao.DatabaseHandler import DatabaseHandler
from reportserver.manager import dateTimeUtility

import dateutil.parser


class IpsManager:

    # Ips Manager: calls necessary managers and utilities to generate parameters for sql.
    #
    validPortNumbers = ()

    def __init__(self):
        self.global_config = Configuration().getInstance()
        self.valid_port_numbers = self.global_config.get_ports()
        self.date_time_field = self.global_config.get_db_datetime_name()


    def get_data(self, ipaddress, uom, unit):
        print("#info Retrieving ipaddress data: " + str(ipaddress) + "  uom:  " + uom + " size: " + str(unit))

        port_data = []

        for port in self.valid_port_numbers:
            results = self.get_json_by_ip(port, ipaddress, uom, unit)
            port_data.append({port:results})

        #results = DatabaseHandler().get_json_by_time(port_number, ipaddress, uom, unit)
        #items = self.process_port_data(results)

        port_json = {
            'ipaddress': str(ipaddress),
            'timespan': uom + "=" + str(unit),
            'ports':port_data
        }

        return port_json


    def process_data(self, results):
        if (results == None or len(results) == 0):
            return results

        #we know we have more than one row
        first_row = results[0]
        current_session = first_row['session']
        port_data_json = [] #object to return at end of day.

        session_json = self.setup_session_json(first_row)  #port_data_json is a list of these
        session_rows= [] #session_json has a list of these

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

    def get_json_by_ip(self, portnumber, ipaddress, uom, units):
        begin_date_iso = dateTimeUtility.get_begin_date_iso(uom, units)
        table_name = self.global_config.get_plugin_config(portnumber)['table']
        date_time_field = self.global_config.get_db_datetime_name()

        #  query = query_db("SELECT * FROM %s where (datetime > '%s')" % (tableName, query_date_iso))
        queryString = "SELECT * FROM %s where %s >= '%s' and localAddress = '%s' order by id, %s" % (
            table_name, date_time_field, begin_date_iso, ipaddress, date_time_field)
        # args = (tableName, date_time_field, begin_date_iso)
        print("#info queryString is: " + str(queryString))
        # print ("args to use: " + str(args))
        results = DatabaseHandler().query_db(queryString)
        print("#debug results: " + str(results))

        return results