from http.server import HTTPServer
import time
from server.PortsServiceHandler import PortsServiceHandler


# TODO: configure these params somewhere else to be edited by admin installer


HOST_NAME="localhost";
PORT_NUMBER=8080;

#Create and start the HTTP Server


class SimpleHttpServer:

    def setupAndStart(self):

        server_addr = (HOST_NAME, PORT_NUMBER)

        # TODO:??  feels wrong to specify PortsServiceHandler here
        # I think we should have PortsServiceHandler havea RequestHandler instead of isa
        request_handler = PortsServiceHandler

        # instantiate a server object
        httpd = HTTPServer (server_addr, request_handler)
        print(time.asctime(), "Server Starting - %s:%s" % (HOST_NAME, PORT_NUMBER))

        try:
            # start serving pages
            httpd.serve_forever ()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print(time.asctime(), "Server Stopped - %s:%s" % (HOST_NAME, PORT_NUMBER))