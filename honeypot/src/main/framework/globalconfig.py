__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import configparser
import os


class GlobalConfig:
    def __init__(self, cfg_path):
        self.cfg_path = cfg_path
        self.plugin_config = configparser.ConfigParser()
        self.config_dictionary = {}

    # ToDo: Dont use eval!
    def create_config_object(self, plugin):
        port = int(self.plugin_config.get(plugin, 'port'))
        table_name = self.plugin_config.get(plugin, 'table')
        enabled = self.plugin_config.get(plugin, 'enabled')
        column_defs = eval(self.plugin_config.get(plugin, 'tableColumns'))
        module = self.plugin_config.get(plugin, 'module')
        rawSocket = self.plugin_config.get(plugin, 'rawSocket')

        config_object = {
            'port': port,
            'table': table_name,
            'enabled': enabled,
            'tableColumns': column_defs,
            'module': module,
            'rawSocket': rawSocket
        }

        return (port, module, config_object)

    def read_config(self, plugin_cfg):
        plugin_config_file = os.path.dirname(
            os.path.abspath(__file__)) + self.cfg_path
        self.plugin_config.read(plugin_config_file)

    def get_sections(self):
        return self.plugin_config.sections()
