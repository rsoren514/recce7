from datetime import datetime, timedelta
from server.UnitOfMeasure import UnitOfMeasure

class Utilities:
    def getIntValue(self, givenStr):
        print("given str is: " + givenStr)
        try:
            returnval = int(givenStr)
            return returnval
        except Exception as e:
            print("received invalid string to convert to int: " + givenStr)
            print (str(e))
            return None

    def getDateRange(self, uom, units):
        currentTime = datetime.now()

        if (uom == UnitOfMeasure.DAY):
            timeBegin = self.getXDaysAgo(currentTime, units)
        #TODO:  implement week, month

        dateList=[timeBegin,currentTime]
        return dateList

    def getXDaysAgo(self, fromTime, units):
        return fromTime - timedelta(days=units);
