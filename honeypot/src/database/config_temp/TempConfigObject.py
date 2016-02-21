#i do not believe i am using this just now

import os
import configparser
from importlib import import_module
'''these methods are temporarily taken from the framework to mimic the reading of a config
file and store them in a config object, this will be useful to reference for validations
for now, in the future the framwork will instantiate the DataManager passing a reference
to itself and we can go after the config object it has already created. Also Randy wanted
to decouple the reading of the config from the starting of the plugins,'''

sub_dir = '/plugins.cfg'
plugin_mods_dir = '../plugins/'


class TempConfigObject:

    def __init__(self, plugin_cfg=None):
        self.config_dictionary = {}
        self.plugin_imports = {}
        self.read_config(plugin_cfg)

    @staticmethod
    def create_config_object(plugin_config, plugin):
        port = int(plugin_config.get(plugin, 'port'))
        column_defs = eval(plugin_config.get(plugin, 'tableColumns'))
        table_name = plugin_config.get(plugin, 'table')
        module = plugin_config.get(plugin, 'module')
        enabled = plugin_config.get(plugin, 'enabled')

        config_object = {
            'port': port,
            'table': table_name,
            'enabled': enabled,
            'tableColumns': column_defs,
            'module': module
        }

        return port, module, config_object



    def read_config(self, plugin_cfg):
        plugin_config_file = os.path.dirname(os.path.abspath(__file__)) + sub_dir
        plugin_config = configparser.ConfigParser()
        plugin_config.read(plugin_config_file)
        plugins = plugin_config.sections()
        for plugin in plugins:
            (port, module, config_object) = self.create_config_object(plugin_config, plugin)
            if config_object['enabled'].lower() == 'yes':
                self.config_dictionary[port] = config_object


    def get_config(self, port):
        return self.config_dictionary[port]

