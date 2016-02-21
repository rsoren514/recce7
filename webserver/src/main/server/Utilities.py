
class Utilities:
    def getIntValue(self, givenStr):
        print("given str is: " + givenStr)
        try:
            returnval = int(givenStr)
            return returnval
        except Exception as e:
            print("received invalid string to convert to int: " + givenStr)
            print (str(e))
            return int(0)