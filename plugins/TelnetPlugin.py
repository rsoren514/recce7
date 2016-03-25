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
import getpass

from plugins.BasePlugin import BasePlugin


class TelnetPlugin(BasePlugin):
    def __init__(self, socket, framework):
        super().__init__(socket, framework)
        self.username = "NULL"
        self.password = "NULL"

    def telnet_login(self):
        user_prompt = "Username: "
        pw_prompt = "Password: "

        for prompt in [user_prompt, pw_prompt]:
            try:
                if prompt == pw_prompt:
                    s = getpass.getpass(prompt.encode())
                    self._skt.sendall(s)
                    self.password = self._skt.recv(1024)
                else:
                    self._skt.send(prompt.encode())
                    self.username = self._skt.recv(1024)
            except OSError as e:
                if not self._skt:
                    # TODO log that the socket was closed
                    pass
                raise e
            except AttributeError as ae:
                # TODO log was not able to capture the either the username or password properly so decode fails
                raise ae

    def display_options(self):
        pass

    def telnet_help(self):
        pass

    def telnet_echo(self, data):
        self._skt.sendall(data)

    def telnet_quit(self):
        pass

    def do_track(self):
        self.telnet_login()
        self.display_options()

        data = ''
        user_input = ''
        # b'' is what I am getting back when the user calls close from the local telnet prompt, may want to look at
        # reading FIN signals from socket somehow, but this works for now
        while not self.kill_plugin:
            self._skt.send(self.username.encode())
            try:
                data = self._skt.recv(1024)
            except OSError as e:
                if not self._skt:
                    break
                raise e

            user_input += '%s' % data.decode('utf-8')

        if self._skt:
            self._skt.send(b'\nGoodbye.\n')
        self._skt = None
        self.form_data_for_insert(user_input)

    def form_data_for_insert(self, raw_data):
        # Would like to be able to read config data from either base or framework if possible, would also like table
        # name derived from elsewhere
        data = {'test_telnet': {'User_Data': raw_data, 'User_Name': self.username, 'Password': self.password}}
        self.do_save(data)
