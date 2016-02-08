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
from scapy import layers
from scapy.all import *
from scapy.layers.inet import IP, TCP


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
            layer_pattern = re.compile('###[(A-Za-z)]###(.*?)None', re.MULTILINE)
            layer_title = layer_pattern.match(p).group(0)
            print(layer_title)
            layer_kvs = layer_pattern.match(p).group(1)
            print(layer_kvs)

        return packets_dict


    def getIpDatagram(self):
        return self.ipDatagramVars

    def getTcpSegment(self):
        return self.tcpSegmentVars

    def verify_insert_statement(self):
        # Read from config how insert statemnt should be and verify against a REGEX
        pass