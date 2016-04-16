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

"""

"""

from plugins.base import BasePlugin


class TelnetPlugin(BasePlugin):
    STATES = ['username',
              'password',
              'command',]

    def __init__(self, socket, config, framework):
        BasePlugin.__init__(self, socket, config, framework)
        self.state = 0
        self.input_type = None
        self.user_input = None
        self._session = str(self.get_uuid4())

    def do_track(self):
        getattr(self, self.STATES[self.state])()

    def get_input(self):
        self.input_type = self.STATES[self.state]
        data = self._skt.recv(1024).decode()
        data = data.strip('\r\n')
        data = data.strip('\n')
        return data

    def username(self):
        try:
            self._skt.send(b'Username: ')
            data = self.get_input()
        except OSError:
            pass
        except AttributeError:
            pass

        self.user_input = data
        self.state += 1

    def password(self):
        try:
            self._skt.send(b'Password: ')
            data = self.get_input()
        except OSError:
            pass
        except AttributeError:
            pass

        self.user_input = data
        self.state += 1
        self.options()

    def command(self):
        self._skt.send(b'. ')
        data = self.get_input()
        try:
            getattr(self, data)()
        except AttributeError:
            self._skt.send(b'Command not supported')
        self.user_input = data

    OPTIONS = ['options',
               'help',
               'echo',
               'quit']

    def options(self):
        self._skt.send(b'\r\nWelcome, Please choose from the following options\r\n')
        for option in self.OPTIONS:
            option += '\t'
            self._skt.sendall(option.encode())
        self._skt.send(b'\r\n')

    def help(self):
        help_msg = b'Command echo:\t\tprompt to echo back typing\r\nCommand help:\t\tdetailed description of ' \
                   b'options\r\nCommand options:\tbasic list of options available to user\r\nCommand quit:\t\t' \
                   b'close telnet connection to server\r\n'
        self._skt.send(help_msg)

    def echo(self):
        self._skt.send(b'text? ')
        try:
            data = self._skt.recv(1024).decode()
        except OSError as e:
            # TODO log error here
            raise e
        self._skt.send(data.encode())

    def quit(self):
        self._skt.send(b'\nGoodbye\n')
        self._skt = None