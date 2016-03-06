from manager.PortManager import PortManager
from server.RESTRequestHandler import RestRequestHandler
from server.UnitOfMeasure import UnitOfMeasure

#todo:  get json from database data
#todo:  set up method for each path
#todo:  decide what we want for path names (what the api will be)



class PortsServiceHandler (RestRequestHandler):

##
    def getPortData(self, portnumber):
        self.getPortDataByTime(portnumber, UnitOfMeasure.DAY, 1)

    def getPortDataByTime(self, portnumber, uom, unit):
        portmgr = PortManager()
        portjsondata = portmgr.getPort(portnumber, uom, unit)
        if portjsondata is not None:
            #send response:
            self.sendJsonResponse(portjsondata, 200)
        else:
            self.notFound();
