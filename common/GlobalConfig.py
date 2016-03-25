import configparser
import os

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>' \
             'Dina Steeve<dsteeve@msudenver.edu>'

#default location of the configuraiton file if an override environment variable not given
#Environment var:  HPOTTR_CONFIG_LOC

default_cfg_path = 'config/plugins.cfg'


class Configuration(object):
    __instance = None


    def __new__(cls):
        print ('new on config was called.')
        if Configuration.__instance is None:
            print("creating new config class")
            Configuration.__instance = object.__new__(cls)
            config_location = os.getenv("HPOTTR_CONFIG_LOC", default_cfg_path)
            Configuration.__instance.val = Configuration.__instance.__read_config(config_location)

        return Configuration.__instance


    #Resturns back an instance of the globalconfig class.
    def getInstance(self):
        return self.__instance.val



    # ToDo: Dont use eval!
    def __create_config_object(self, plugin, config_parser):
        port = int(config_parser.get(plugin, 'port'))
        table_name = config_parser.get(plugin, 'table')
        enabled = config_parser.get(plugin, 'enabled')
        column_defs = eval(config_parser.get(plugin, 'tableColumns'))
        module = config_parser.get(plugin, 'module')
        raw_socket = config_parser.get(plugin, 'rawSocket')

        config_object = {
            'port': port,
            'table': table_name,
            'enabled': enabled,
            'tableColumns': column_defs,
            'module': module,
            'rawSocket': raw_socket
        }

        return port, module, config_object

    def __read_config(self, cfg_path):
        print("Reading the plugin config file: " + cfg_path)
        config_parser = configparser.ConfigParser()
        plugin_config_file = cfg_path

        config_parser.read(plugin_config_file)

        config_dictionary= {}
        enabled_ports = []

        plugins = config_parser.sections()
        for plugin in plugins:
            (port, module, config_object) = self.__create_config_object(plugin,config_parser)
            if config_object['enabled'].lower() == 'yes':
                config_dictionary[port] = config_object
                enabled_ports.append(port)

        #Todo:  read in report server config
        rserver_dictionary={"host":"localhost", "port":8080}

        return GlobalConfig(config_dictionary, enabled_ports, rserver_dictionary)


##The actual thing that holds the configuration data in the *.cfg file
class GlobalConfig:
    def __init__(self, plugin_dictionary, ports, rs_dictionary):
        self.__plugin_dictionary = plugin_dictionary
        self.__enabled_ports = ports
        self.__rserver_dictionary = rs_dictionary

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
        return self.__enabled_ports.copy()

    '''
    Returns the configuration dictionary for the plugin listening
    on the specified port.

    :param port: an integer specifying a TCP/IP port
    :return: a dictionary with the config file parameters for the
             plugin that listens on port
    '''
    def get_plugin_config(self, port):
        return self.__plugin_dictionary[port]

    def get_plugin_dictionary(self):
        return self.__plugin_dictionary

    def get_report_server_host(self):
        return self.__rserver_dictionary["host"]

    def get_report_server_port(self):
        return self.__rserver_dictionary["port"]