from reportserver.manager.PortManager import PortManager
from reportserver.manager import utilities
from common.GlobalConfig import Configuration



class PortsServiceHandler():

    def process(self, rqst, path_tokens, query_tokens):
        uom = None
        units = None
        print("processing ports request:" + str(path_tokens) + str(query_tokens))

        if len(query_tokens) > 0:
            try:
                time_period = utilities.validate_time_period(query_tokens)
                uom = time_period[0]
                units = time_period[1]
            except ValueError:
                rqst.badRequest(units)
                return

        if len(path_tokens) == 5:
            portNbr = utilities.validate_port_number(path_tokens[4])
            print("requested: " + str(portNbr))
            if portNbr is not None and 0 < portNbr < 9000:
                self.get_port_data_by_time(rqst, portNbr, uom, units)
            else:
                rqst.badRequest()
                return
        elif len(path_tokens) == 4:
            self.get_port_list_json(rqst)
        else:
            rqst.badRequest()
            return


    def get_port_list_json(self,rqst):
        jsondata = self.construct_port_summary_list(rqst)
        rqst.sendJsonResponse(jsondata, 200)

    def get_port_data_by_time(self, rqst, portnumber, uom, unit):
        #default if we aren't given valid uom and unit
        if uom is None or unit is None:
            uom = "days"
            unit = 1

        portmgr = PortManager()
        portjsondata = portmgr.getPort(portnumber, uom, unit)
        if portjsondata is not None:
            # send response:
            rqst.sendJsonResponse(portjsondata, 200)
        else:
            rqst.notFound()

    def construct_port_summary_list(self, rqst):
        g_config = Configuration().getInstance()
        plugins_dictionary = g_config.get_plugin_dictionary()

        json_list = []
        for key, val in plugins_dictionary.items():
            json_list.append(self.construct_port_summary(rqst, val['port'], val['table']))

        return json_list

    def construct_port_summary(self, rqst, portnumber, tablename):
        portmgr = PortManager()
        port_attacks = portmgr.get_port_attack_count(tablename)
        unique_ips = portmgr.get_unique_ips(tablename)

        response_json = {
            'port': str(portnumber),
            'total_attacks': str(port_attacks),
            'unique_ipaddresses': str(unique_ips),
            'rel_link': rqst.get_full_url_path() + "/ports/" + str(portnumber)
        }

        return response_json