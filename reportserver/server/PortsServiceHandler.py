from reportserver.manager.PortManager import PortManager
from reportserver.manager import utilities



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
            self.get_port_list(rqst)
        else:
            rqst.badRequest()
            return


    def get_port_list(self,rqst):
        #todo:  finish this!
        jsondata = "{links : [under construction]}"
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
