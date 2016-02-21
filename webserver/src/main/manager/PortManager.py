class PortManager ():
    fakePort80DataWithTime = {
        'port': '80',
        'attackerData': 'some clever string here',
        'datetimestamp': '2016-02-14:13:14:22MST'
    }


    def getPort(self,portNumber, uom, unit):
        print("retrieving port:" + str(portNumber))

        if (portNumber == 80):
            return self.fakePort80DataWithTime
        else:
            return None


