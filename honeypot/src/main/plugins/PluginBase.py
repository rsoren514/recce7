################################################################################
#                                                                              #
#                           GNU Public License v3.0                            #
#                                                                              #
################################################################################
#   HunnyPotRx is a honeypot designed to be a one click installable,           #
#   open source honey-pot that any developer or administrator would be able    #
#   to write custom plugins for based on specific needs.                       #
#   Copyright (C) 2016 RECCE7                                                  #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See their            #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public licenses         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
################################################################################

from scapy.all import *


class PluginBase():
    # Variables passed in from Framework
    rawPacket = None
    portNumber = None
    callbackMethod = None

    def __init__(self, rawPacket=None, portNumber=None, callBack=None):
        self.rawPacket = rawPacket
        self.portNumber = portNumber
        self.callbackMethod = callBack
        self.parse_packet(rawPacket)
        # Logic to check port number in config file and start plugin from info there

    def parse_packet(self, packets):
        # Use scapy to break packets into appropriate pieces, change values of variables
        packets_dict = None
        for p in packets:
            pkt = p.command()
            layers = re.split('\/', pkt)
            for l in layers:
                layer = re.match('(\w+)[\(]', l)
                if layer != None and layer != 'Raw':
                    layer = layer.group(1)
                    print(layer)
                # else:
                #     print('Error Printing, LAYER:\n' +layer + '\nPACKET:\n' + pkt)

            print(pkt)

        return packets_dict


    def getIpDatagram(self):
        return self.ipDatagramVars

    def getTcpSegment(self):
        return self.tcpSegmentVars

    def verify_insert_statement(self):
        # Read from config how insert statemnt should be and verify against a REGEX
        pass
