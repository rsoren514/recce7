from reportserver.manager.IpsManager import IpsManager
from reportserver.manager import utilities
from common.logger import Logger


badIpAddress = {
    'error': 'invalid ipaddress given'}

class WorldmapServiceHandler():
    def __init__(self):
        self.log = Logger().get('reportserver.manager.WorldmapServiceManager.py')

    def process(self, rqst, path_tokens, query_tokens):
        uom = None
        units = None
        self.log.info("processing ipaddress request:" + str(path_tokens) + str(query_tokens))


        try:
            time_period = utilities.validate_time_period(query_tokens)
            uom = time_period[0]
            units = time_period[1]
        except ValueError:
            rqst.badRequest(units)
            return


        if len(path_tokens) >= 5:
            rqst.badRequest()
            return


    def get_ips_latlong_by_time(self, rqst, ipaddress, uom, units):
        #TODO: implement me!

        rqst.sendPngResponse("./test.png", 200)
