import configparser
import os

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'


class GlobalConfig:
    def __init__(self, cfg_path):
        self.cfg_path = cfg_path
        self.plugin_config = configparser.ConfigParser()
        self.config_dictionary = {}
        self.enabled_ports = []

    # ToDo: Dont use eval!
    def create_config_object(self, plugin):
        port = int(self.plugin_config.get(plugin, 'port'))
        table_name = self.plugin_config.get(plugin, 'table')
        enabled = self.plugin_config.get(plugin, 'enabled')
        column_defs = eval(self.plugin_config.get(plugin, 'tableColumns'))
        module = self.plugin_config.get(plugin, 'module')
        raw_socket = self.plugin_config.get(plugin, 'rawSocket')

        config_object = {
            'port': port,
            'table': table_name,
            'enabled': enabled,
            'tableColumns': column_defs,
            'module': module,
            'rawSocket': raw_socket
        }

        return port, module, config_object

    def read_config(self):
        plugin_config_file = self.cfg_path
        self.plugin_config.read(plugin_config_file)

        plugins = self.plugin_config.sections()
        for plugin in plugins:
            (port, module, config_object) = self.create_config_object(plugin)
            if config_object['enabled'].lower() == 'yes':
                self.config_dictionary[port] = config_object
                self.enabled_ports.append(port)

    #
    # Config API
    #

    '''
    Returns a string indicating the location where the SQLite
    database file will be stored.

    :return: a string containing an absolute path
    '''
    def get_db_dir(self):
        return os.getenv('HOME') + '/honeyDB'

    '''
    Returns a list of ports with enabled plugins listening.

    :return: a list of integers representing TCP/IP ports
    '''
    def get_ports(self):
        return self.enabled_ports.copy()

    '''
    Returns the configuration dictionary for the plugin listening
    on the specified port.

    :param port: an integer specifying a TCP/IP port
    :return: a dictionary with the config file parameters for the
             plugin that listens on port
    '''
    def get_plugin_config(self, port):
        return self.config_dictionary[port]
