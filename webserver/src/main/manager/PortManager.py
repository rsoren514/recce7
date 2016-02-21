class PortManager ():
    fakePort80DataWithTime = {
        'port': '80',
        'attackerData': 'some clever string here',
        'datetimestamp': '2016-02-14:13:14:22MST'
    }

    #TODO:
    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    #  Mgr for reading config files to know what table /column names there are.
    #  Utilitity for calc time range
    #
    # calls calls PortDao with sql string.
    # PortDao, will extend from a base class that knows how to connect to database.
    # PortDao:  will run sql and return json

    def getPort(self,portNumber, uom, unit):
        print("retrieving port:" + str(portNumber))

        if (portNumber == 80):
            return self.fakePort80DataWithTime
        else:
            return None


