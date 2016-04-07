import json
from http.server import BaseHTTPRequestHandler


from reportserver.server.PortsServiceHandler import PortsServiceHandler


notFoundPayload = {}

badRequestPayload = {
    'error': 'invalid port number'}


#  Handles the service request, determines what was requested,
#  then returns back response.
#
class RestRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        tokens = self.path.split('/')
        print(tokens)

        if self.path.startswith("/v1/analytics/"):
            if len(tokens) >= 4:
                print ("4th token: " + tokens[3])
                if str(tokens[3]) == "ports":
                    PortsServiceHandler().process(self, tokens)
                else:
                    print ("token[3] is: " + str(tokens[3]))
                    self.badRequest()
        else:
            self.notFound()



    def getIndexPayload(self, path):
        #TODO:  how to get full path here??
        return  {'links': ['rel: ports, href:' + path + 'ports']}

    def showIndex(self,path):
        # send response code:
        self.sendJsonResponse(self.getIndexPayload(path), 200)

    def notFound(self):
        # send response code:
        self.sendJsonResponse(notFoundPayload,404)

    def badRequest(self):
        # send response code:
        self.sendJsonResponse(badRequestPayload,400)

    def sendJsonResponse(self, payload, responseCode):

        # Note:  responseCode must be set before headers in python3!!
        # see this post:
        # http://stackoverflow.com/questions/23321887/python-3-http-server-sends-headers-as-output/35634827#35634827
        json_result = json.dumps(payload)
        self.send_response(responseCode)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_result))
        self.end_headers()
        self.flush_headers()

        self.wfile.write(bytes(json_result, "utf-8"))

        self.wfile.flush()

        return




