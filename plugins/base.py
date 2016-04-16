"""
Plugin base class

Contents
- BasePlugin: Base class for all plugins.
"""

import platform
import socket
import datetime
from threading import Thread


class BasePlugin(Thread):
    """

    """
    def __init__(self, socket, config, framework):
        """

        """
        Thread.__init__(self)
        self._skt = socket
        self._config = config
        self._framework = framework
        self._localAddress = self.get_host_address()
        self._peerAddress = self.get_client_address()
        self._session = None
        self.kill_plugin = False

    def run(self):
        """

        """
        while self._skt and not self.kill_plugin:
            try:
                print(self.get_table_columns())
                self.do_track()
                self.do_save()
            except ConnectionResetError as cre:
                error_number = cre.errno
                if error_number == 54:  # ERRNO 54 is 'connection reset by peer'
                    # Log that it is possible we are being scanned, would want to write this to the db
                    print("Maybe we are being scanned")
                    pass

        self._framework.plugin_stopped(self)

    def do_save(self):
        entry = {self.get_table_name() : {}}
        columns = self.get_table_columns()

        for i in columns:
            try:
                entry[self.get_table_name()][i] = getattr(self, i)
            except AttributeError:
                entry[self.get_table_name()][i] = 'Attribute did not exist'

        self._framework.insert_data(entry)

    '''def do_save(self, data):
        """

        """
        data_malformed = False
        #Add default values for all plugins
        keys = list(data.keys())
        # Should only be one key for the table name in the outer dictionary
        if len(keys) == 1:
            data_values_list = list(data.values())
            # Should only be one (inner) dictionary for the key
            if len(data_values_list) == 1:
                data_values = data_values_list[0]
                data_values['peerAddress'] = self._peerAddress
                data_values['localAddress'] = self._localAddress
                data_values['eventDateTime'] = datetime.datetime.now().isoformat()
                #data_values['session'] = self._session
                self._framework.insert_data({keys[0]:data_values})
            else:
                data_malformed = True
                pass
        else:
            data_malformed = True
            pass

        if data_malformed:
            print("Data to be inserted from plugin is malformed: " + self.name)
            #TODO log here
            self.shutdown()'''

    def shutdown(self):
        """

        """
        self.kill_plugin = True

        if self._skt:
            old_skt = self._skt
            self._skt = None
            if platform.system() == 'Linux':
                old_skt.shutdown(socket.SHUT_RDWR)
                old_skt.detach()
            old_skt.close()
        else:
            print("Socket already closed for plugin thread name: " + self.name)

        self.join()

    def do_track(self):
        """
        Implemented by the plugin writer.
        """
        pass

    def get_session(self):
        """
        Implemented by the plugin writer.
        """
        pass

    def get_plugin_port(self):
        """
        Returns the port for this plugin.
        """
        return self._config['port']

    def get_host_address(self):
        """
        Returns the host's ip address.
        """
        return self._skt.getsockname()[0]

    def get_client_address(self):
        """
        Returns the client's ip address.
        """
        return self._skt.getpeername()[0]

    def get_table_name(self):
        """
        Returns the database table name for this plugin.
        """
        return self._config['table']

    def get_table_columns(self):
        """
        Returns the column names for this plugin.
        """
        print(self._config)
        print(self._config['tableColumns'])
        columns = []

        for i in self._config['tableColumns']:
            columns.append(i[1])

        return columns
