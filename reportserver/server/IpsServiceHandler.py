from reportserver.manager.IpsManager import IpsManager
from reportserver.manager import utilities
from common.GlobalConfig import Configuration



class IpsServiceHandler():

    def process(self, rqst, path_tokens, query_tokens):
        uom = None
        units = None
        print("#info processing ipaddress request:" + str(path_tokens) + str(query_tokens))

        if len(query_tokens) > 0:
            try:
                time_period = utilities.validate_time_period(query_tokens)
                uom = time_period[0]
                units = time_period[1]
            except ValueError:
                rqst.badRequest(units)
                return

        # default if we aren't given valid uom and units
        if uom is None or units is None:
            uom = "days"
            units = 1

        if len(path_tokens) == 5:
            ipaddress = utilities.validate_ipaddress(path_tokens[4])
            print("#debug requested: " + str(ipaddress))
            if ipaddress is not None :
                self.get_ips_data_by_time(rqst, ipaddress, uom, units)
            else:
                rqst.badRequest()
                return
        elif len(path_tokens) == 4:
            self.get_ips_list_json(rqst, uom, units)
        else:
            rqst.badRequest()
            return


    def get_ips_data_by_time(self, rqst, ipaddress, uom, units):

        ips_manager = IpsManager()
        addressjsondata = ips_manager.get_data(ipaddress, uom, units)
        if addressjsondata is not None:
            # send response:
            rqst.sendJsonResponse(addressjsondata, 200)
        else:
            rqst.notFound()

    def get_ips_list_json(self, rqst, uom, units):
        response = "{not implemented yet.}"
        rqst.sendJsonResponse(response,200)