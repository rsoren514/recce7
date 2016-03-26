from common.GlobalConfig import Configuration
import unittest
import os

class GlobalConfig_Test(unittest.TestCase):
    def setUp(self):
        self.gconfig = Configuration("./test.cfg").getInstance()

    def test_getInstance(self):

        gconfig2 = Configuration().getInstance()

        self.assertEqual(str(self.gconfig),str(gconfig2),"these 2 objects should equal")

        gconfig3 = Configuration().getInstance()

        self.assertEqual(str(self.gconfig), str(gconfig3), "these 2 objects should equal")
        self.assertEqual(str(gconfig2), str(gconfig3), "these 2 objects should equal")


    def test_getPorts(self):

        ports = self.gconfig.get_ports()

        self.assertEquals(len(ports), 2, "expected 2 ports in test.cfg found: " + str(len(ports)))

        for port in ports:
            print("found: " + str(port))

    def test_getReportServerConfig(self):
        host = self.gconfig.get_report_server_host()
        port = self.gconfig.get_report_server_port()
        self.assertEquals(host, "localhost", "expected host to be 'localhost'")
        self.assertEquals(port, 8080, "expected port to be '8080' ")

if __name__ == "__main__":
    unittest.main()
