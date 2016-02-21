import unittest
from server.PortsServiceHandler import PortsServiceHandler

def fun(x):
    return x + 1

class PortsServiceHandlerTest(unittest.TestCase):
    def testSanity(self):
        self.assertEqual(fun(3), 4)

    def testGetPort(self):
        portsServiceHandler = PortsServiceHandler()
        response = portsServiceHandler.getPort(80);
        self.assertEqual(response, None);

