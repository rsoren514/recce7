from reportserver.server.RESTRequestHandler import RestRequestHandler

from reportserver.manager.PortManager import PortManager


# Todo:  set up method for each path
# Todo:  decide what we want for path names (what the api will be)


class PortsServiceHandler (RestRequestHandler):

    def getPortData(self, portnumber):
        # default is one day if not specified
        self.getPortDataByTime(portnumber, "days", 1)

    def getPortDataByTime(self, portnumber, uom, unit):
        portmgr = PortManager()
        portjsondata = portmgr.getPort(portnumber, uom, unit)
        if portjsondata is not None:
            # send response:
            self.sendJsonResponse(portjsondata, 200)
        else:
            self.notFound();
