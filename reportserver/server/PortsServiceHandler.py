from reportserver.manager.PortManager import PortManager




class PortsServiceHandler ():

    def getPortDataByTime(self, rqst, portnumber, uom, unit):
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
