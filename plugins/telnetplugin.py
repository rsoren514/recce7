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

from plugins.base import BasePlugin


class TelnetPlugin(BasePlugin):
    def telnet_login(self):
        pass

    def telnet_help(self):
        pass

    def telnet_echo(self):
        pass

    def telnet_quit(self):
        pass

    def do_track(self):
        welcome = 'Welcome to %s\n' % self._localAddress
        self._skt.send(welcome.encode())

        self.telnet_login()

        escape = b'\x1e'
        data = ''
        self.user_input = 'BEGIN USER DATA ::'
        # b'' is what I am getting back when the user calls close from the local telnet prompt, may want to look at
        # reading FIN signals from socket somehow, but this works for now
        while data != escape and data != b'':
            try:
                data = self._skt.recv(1024)
            except OSError as e:
                if not self._skt:
                    break
                raise e

            self.user_input += '\n%s' % data
            self._skt.sendall(data)

        if self._skt:
            self._skt.send(b'\nGoodbye.\n')
        self._skt = None
        self.form_data_for_insert(self.user_input)

    def form_data_for_insert(self, raw_data):
        # Would like to be able to read config data from either base or framework if possible, would also like table
        # name derived from elsewhere
        data = {'test_telnet': {'User_Data': raw_data, 'Test_col': 'This is a test'}}
        self.do_save(data)
