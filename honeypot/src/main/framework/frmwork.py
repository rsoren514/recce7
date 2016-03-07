__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

from database.DataManager import DataManager
from framework.globalconfig import GlobalConfig
from framework.networklistener import NetworkListener

from importlib import import_module

default_cfg_path = '/config/plugins.cfg'


class Framework:
    def __init__(self, cfg_path):
        self.global_config = GlobalConfig(cfg_path)
        self.plugin_imports = {}
        self.data_manager = None

    def start(self):
        self.global_config.read_config()
        self.data_manager = DataManager(self.global_config)
        self.start_plugins()

    def create_import_entry(self, port, name):
        imp = import_module('plugins.' + name)
        self.plugin_imports[port] = getattr(imp, name)

    def start_plugins(self):
        ports = self.global_config.get_ports()
        print("the ports are: " + str(ports))
        for port in ports:
            print("spawing this port:" + str(port))
            plugin_config = self.global_config.get_plugin_config(port)
            module = plugin_config['module']
            self.create_import_entry(port, module)
            listener = NetworkListener(plugin_config, self)
            listener.start()

    #
    # Framework API
    #

    '''
    Returns the configuration dictionary for the plugin
    running on the specified port.

    :param port: a port number associated with a loaded plugin
    :return: a plugin configuration dictionary
    '''
    def get_config(self, port):
        return self.global_config.get_plugin_config(port)

    '''
    Spawns the plugin configured by 'config' with the provided
    (accepted) socket.

    :param socket: an open, accepted socket returned by
                   socket.accept()
    :param config: the plugin configuration dictionary describing
                   the plugin to spawn
    '''
    def spawn(self, socket, config):
        # ToDo Throw exception if plugin class not found
        plugin_class = self.plugin_imports[config['port']]
        plugin = plugin_class(socket, self)

    '''
    Inserts the provided data into the data queue so that it can
    be pushed to the database.

    :param data: data object to add to the database
    '''
    def insert_data(self, data):
        self.data_manager.insert_data(data)


#def main(cfg_path=None):
#    framework = Framework(cfg_path or default_cfg_path)
#    framework.start()

#if __name__ == '__main__': main()
