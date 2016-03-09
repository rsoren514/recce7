from dao import DatabaseHandler

class PortManager ():

    #TODO:
    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    #  Mgr for reading config files to know what table /column names there are.
    #  Utilitity for calc time range
    #
    #

    def getPort(self,portNumber, uom, unit):
        print("retrieving port:" + str(portNumber))

        if (portNumber == 80):
            # return self.fakePort80DataWithTime
            return DatabaseHandler.getJson(portNumber, uom, unit);
        else:
            return None


