import configparser
import os

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>' \
             'Dina Steeve <dsteeve@msudenver.edu>'

default_cfg_path = 'config/plugins.cfg'

# TODO: currently can't override this one
default_global_cfg_file = 'config/global.cfg'


class GlobalConfig:
    __instance = None
    class __GlobalConfig:
        def __init__(self, plugin_cfg_path, global_cfg_path):
            self._plugin_cfg_path = plugin_cfg_path
            self._global_cfg_path = global_cfg_path

            self._plugin_cfg_dict = {}
            self._db_cfg_dict = {}
            self._report_server_cfg_dict = {}

            self._enabled_ports = []

        def _create_plugin_dict(self, plugin, config_parser):
            port = int(config_parser.get(plugin, 'port'))
            table_name = config_parser.get(plugin, 'table')
            enabled = config_parser.get(plugin, 'enabled')
            # TODO: Don't use eval!
            column_defs = eval(config_parser.get(plugin, 'tableColumns'))
            module = config_parser.get(plugin, 'module')
            module_class = config_parser.get(plugin, 'moduleClass')
            raw_socket = config_parser.get(plugin, 'rawSocket')

            config_object = {
                'port': port,
                'table': table_name,
                'enabled': enabled,
                'tableColumns': column_defs,
                'module': module,
                'moduleClass': module_class,
                'rawSocket': raw_socket
            }

            return port, module, config_object

        def read_plugin_config(self):
            config_parser = configparser.ConfigParser()
            config_parser.read(self._plugin_cfg_path)

            plugin_sections = config_parser.sections()
            for plugin in plugin_sections:
                (port, module, config_object) = \
                    self._create_plugin_dict(plugin, config_parser)
                if config_object['enabled'].lower() == 'yes':
                    self._plugin_cfg_dict[port] = config_object
                    self._enabled_ports.append(port)

        def read_global_config(self):
            config_parser = configparser.ConfigParser()
            config_parser.read(default_global_cfg_file)

            self._report_server_cfg_dict = \
                config_parser['ReportServerSection']
            self._db_cfg_dict = config_parser['DatabaseSection']

        #
        # Config API
        #

        def get_plugin_dictionary(self):
            return self._plugin_cfg_dict

        def get_db_name(self):
            return self._db_cfg_dict["database.name"]

        def get_db_dir(self):
            """
            Returns a string indicating the location where the SQLite
            database file will be stored.

            :return: a string containing an absolute path
            """
            db_dir = os.getenv('RECCE7_DB_PATH') or os.getenv('HOME') or '.'
            return db_dir + '/' + self.get_db_name()

        def get_db_datetime_name(self):
            return self._db_cfg_dict["database.datetime.name"]

        def get_db_peerAddress_name(self):
            return self._db_cfg_dict["database.peerAddress.name"]

        def get_db_localAddress_name(self):
            return self._db_cfg_dict["database.localAddress.name"]

        def get_ports(self):
            """
            Returns a list of ports with enabled plugins listening.

            :return: a list of integers representing TCP/IP ports
            """
            return self._enabled_ports.copy()

        def get_plugin_config(self, port):
            """
            Returns the configuration dictionary for the plugin listening
            on the specified port.

            :param port: an integer specifying a TCP/IP port
            :return: a dictionary with the config file parameters for the
                     plugin that listens on port
            """
            return self._plugin_cfg_dict[port]

        def get_report_server_host(self):
            return self._report_server_cfg_dict["reportserver.host"]

        def get_report_server_port(self):
            port = self._report_server_cfg_dict["reportserver.port"]
            return int(port)

    def __new__(cls, plugin_cfg_path=None, global_cfg_path=None, refresh=False):
        """
        Returns the configuration singleton, or instantiates it
        if: 1) no instance exists yet, or 2) the refresh parameter
        is True.

        :param plugin_cfg_path: A string containing the path to
                                the plugin configuration file.
        :param global_cfg_path: A string containing the path to
                                the global/program configuration
                                file.
        :param refresh: When True, any current instance will be replaced by a
                        new instance (useful for unit testing).
        :return: A GlobalConfig instance.
        """
        if refresh or not GlobalConfig.__instance:
            GlobalConfig.__instance = GlobalConfig.__GlobalConfig(
                plugin_cfg_path, global_cfg_path)
        return GlobalConfig.__instance

    def __getattr__(self, name):
        return getattr(GlobalConfig.__instance, name)

    def __setattr__(self, name, value):
        return setattr(GlobalConfig.__instance, name, value)
