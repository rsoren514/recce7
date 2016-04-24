import json
from reportserver.manager import utilities
from http.server import BaseHTTPRequestHandler


from reportserver.server.PortsServiceHandler import PortsServiceHandler
from reportserver.server.IpsServiceHandler import IpsServiceHandler



notFoundPayload = {}

badRequestPayload = {
    'error': 'invalid analytics request'}


#  Handles the service request, determines what was requested,
#  then returns back response.
#
class RestRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        path_query_tuple = utilities.get_path_query_tokens(self.path)
        path_tokens = path_query_tuple[0]
        query_tokens = path_query_tuple[1]

        if self.path.startswith("/v1/analytics"):
            if len(path_tokens) >= 4:
                if str(path_tokens[3]) == "ports":
                    PortsServiceHandler().process(self, path_tokens, query_tokens)
                elif str(path_tokens[3]) == "ipaddresses":
                    IpsServiceHandler().process(self, path_tokens, query_tokens)
                else:
                    self.badRequest()
            else:
                self.showIndex()
        else:
            self.notFound()



    def get_full_url_path(self):
        # TODO:  how to get full path here??
        print("address : " + str(self.client_address))
        full_path = 'http://%s:%s/v1/analytics' % (str(self.client_address[0]), str(8080))
        return full_path

    def getIndexPayload(self):
        return  {'links': ['rel: ports, href: ' + self.get_full_url_path() + '/ports',
                           'rel: ipaddress, href:' + self.get_full_url_path() + '/ipaddresses']}

    def showIndex(self):
        # send response code:
        self.sendJsonResponse(self.getIndexPayload(), 200)

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
        #todo make this configurable for allow-origin
        self.send_header("Access-Control-Allow-Origin","http://localhost:8000")
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_result))
        self.end_headers()
        self.flush_headers()

        self.wfile.write(bytes(json_result, "utf-8"))

        self.wfile.flush()

        return




