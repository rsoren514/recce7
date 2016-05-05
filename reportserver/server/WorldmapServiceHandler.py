import matplotlib.pyplot as plt
import numpy as np
import os.path
import pickle
import sqlite3

from common.globalconfig import GlobalConfig
from common.logger import Logger
from mpl_toolkits.basemap import Basemap
from reportserver.manager.IpsManager import IpsManager
from reportserver.manager import dateTimeUtility
from reportserver.manager import utilities


badIpAddress = {
    'error': 'invalid ipaddress given'}

pickle_file = '/mnt/vol1-linux/ip_map.pickle'
pickle_bytes = None
def preload_map():
    if not os.path.isfile(pickle_file):
        ip_map = Basemap(projection='robin', lon_0=0, resolution='c')
        ip_map.drawlsmask(ocean_color="#99ccff", land_color="#009900")
        ip_map.drawcountries(linewidth=0.25, color='#ffff00')
        ip_map.drawcoastlines(linewidth=0.25)
        pickle.dump(ip_map, open(pickle_file, 'wb'), -1)
    else:
        ip_map = pickle.load(open(pickle_file, 'rb'))

    global pickle_bytes
    pickle_bytes = pickle.dumps(ip_map, -1)
preload_map()


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

        ip_map = pickle.loads(pickle_bytes)

        pts = self.get_point_list(uom, units)
        for pt in pts:
            srclat, srclong = pt
            x, y = ip_map(srclong, srclat)
            plt.plot(x, y, 'o', color='#ff0000', ms=1.0, markeredgewidth=0.3)

        plt.savefig('reportserver/worldmap.png', dpi=600)
        rqst.sendPngResponse("reportserver/worldmap.png", 200)

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




