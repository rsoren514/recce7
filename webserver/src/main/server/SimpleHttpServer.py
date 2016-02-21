from http.server import HTTPServer
import time

from PortsServiceHandler import *

# TODO: configure these params somewhere else to be edited by admin installer

HOST_NAME="localhost";
PORT_NUMBER=8080;

#Create and start the HTTP Server

class SimpleHttpServer():
    def setupAndStart(self):

        server_addr = (HOST_NAME, PORT_NUMBER)

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