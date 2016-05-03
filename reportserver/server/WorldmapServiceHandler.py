from reportserver.manager.IpsManager import IpsManager
from reportserver.manager import utilities
from common.logger import Logger
from common.globalconfig import GlobalConfig


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
        else:
            self.construct_worldmap(rqst, uom, units)

    def construct_worldmap(self, rqst, uom, units):
        #call to construct port list
        #find unique ips by port
        #merge the results togoether
        #build the map
        #probably want to look at the PortsServiceHandler.py or IpsServiceHandler.py to follow those patterns.

        rqst.sendPngResponse("reportserver/test.png", 200)



