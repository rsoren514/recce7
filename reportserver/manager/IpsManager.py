
from common.GlobalConfig import Configuration
from reportserver.dao.DatabaseHandler import DatabaseHandler
from reportserver.manager import dateTimeUtility
from reportserver.manager import utilities

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
            items = utilities.process_data(results)
            port_data.append({port:items})

        port_json = {
            'ipaddress': str(ipaddress),
            'timespan': uom + "=" + str(unit),
            'ports':port_data
        }

        return port_json




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