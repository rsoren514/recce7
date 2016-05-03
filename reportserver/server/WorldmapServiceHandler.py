from reportserver.manager.IpsManager import IpsManager
from reportserver.manager import utilities
from common.logger import Logger
from common.globalconfig import GlobalConfig
from reportserver.manager import dateTimeUtility
import sqlite3

badIpAddress = {
    'error': 'invalid ipaddress given'}

class WorldmapServiceHandler():
    def __init__(self):
        self.log = Logger().get('reportserver.manager.WorldmapServiceManager.py')
        self.global_config = GlobalConfig()
        self.global_config.read_plugin_config()
        self.global_config.read_global_config()

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

    def get_point_list(self, uom, units):
        begin_date = dateTimeUtility.get_begin_date_iso(uom, units)
        query_string = ('select lat,long '
                        'from ('
                            'select distinct lat,long,timestamp, ip '
                            'from ipInfo '
                            'where lat is not null '
                            'and long is not null '
                            'and datetime(timestamp) > datetime(\'' + begin_date + '\')'
                            ');')
        connection = sqlite3.connect(self.global_config['Database']['path'])
        cursor = connection.cursor()
        return cursor.execute(query_string).fetchall()




