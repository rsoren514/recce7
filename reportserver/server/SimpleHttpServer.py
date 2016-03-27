import time
from common.GlobalConfig import Configuration
from http.server import HTTPServer

from reportserver.server.PortsServiceHandler import PortsServiceHandler


#Create and start the HTTP Server


class SimpleHttpServer:
    def __init__(self):
        self.g_config = Configuration().getInstance()
        self.host = self.g_config.get_report_server_host()
        self.port = self.g_config.get_report_server_port()


    def setupAndStart(self):


        server_addr = (self.host, self.port)

        # TODO:??  feels wrong to specify PortsServiceHandler here
        # I think we should have PortsServiceHandler havea RequestHandler instead of isa
        request_handler = PortsServiceHandler

        # instantiate a server object
        httpd = HTTPServer (server_addr, request_handler)
        print(time.asctime(), "Server Starting - %s:%s" % (self.host, self.port))

        try:
            # start serving pages
            httpd.serve_forever ()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print(time.asctime(), "Server Stopped - %s:%s" % (self.host, self.port))