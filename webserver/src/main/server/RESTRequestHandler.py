from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from manager.PortManager import PortManager
import json

#todo:  get json from database data
#todo:  set up method for each path
#todo:  decide what we want for path names (what the api will be)

fakejson = {"test": "something"}


class RESTRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        print self.path.split('/')

        if self.path == "/analytics/ports" :
            self.getPort(80)
        else :
            self.notFound()


##
    def notFound(self):
        #send response code:
        self.send_response(404)
        self.sendJsonResponse("Not Found")

    def getPort(self, portnumber):
        portmgr = PortManager()
        portjsondata = portmgr.getPort(portnumber)
        #send response code:
        self.send_response(200)
        self.sendJsonResponse(portjsondata)



    def sendJsonResponse(self, payload):
        self.send_header("Content-type:", "text/html")
        # send a blank line to end headers:
        self.wfile.write("\n")
        #send response:
        json.dump(payload, self.wfile)

