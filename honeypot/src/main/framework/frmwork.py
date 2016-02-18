__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import configparser
import os

# from main.plugins.BasePlugin import *
from networklistener import NetworkListener
from importlib import import_module

sub_dir = '/config/plugins.cfg'
plugin_mods_dir = '../plugins/'


class Framework:
    def __init__(self, plugin_cfg=None):
        self.config_dictionary = {}
        self.plugin_imports = {}
        self.read_config(plugin_cfg)

    #ToDo: Dont use eval!
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

        return (port, module, config_object)

    def create_import_entry(self, port, name):
        imp = import_module('plugins.' + name)
        self.plugin_imports[port] = getattr(imp, name)

    def read_config(self, plugin_cfg):
        plugin_config_file = os.path.dirname(os.path.abspath(__file__)) + (plugin_cfg or sub_dir)
        plugin_config = configparser.ConfigParser()
        plugin_config.read(plugin_config_file)

        plugins = plugin_config.sections()
        for plugin in plugins:
            (port, module, config_object) = self.create_config_object(plugin_config, plugin)
            if config_object['enabled'].lower() == 'yes':
                self.config_dictionary[port] = config_object
                self.create_import_entry(port, module)
                listener = NetworkListener(config_object, self)
                listener.start()

    def get_config(self, port):
        return self.config_dictionary[port]

    #ToDo Throw exception if plugin class not found
    def spawn(self, socket, config):
        plugin_class = self.plugin_imports[config['port']]
        plugin = plugin_class(socket)
        plugin.start()

if __name__ == '__main__':
    framework = Framework()

