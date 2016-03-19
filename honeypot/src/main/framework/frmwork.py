__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

from database.DataManager import DataManager
from framework.globalconfig import GlobalConfig
from framework.networklistener import NetworkListener

from importlib import import_module

import grp
import os
import pwd

import signal

import platform

default_cfg_path = '/config/plugins.cfg'


class Framework:
    def __init__(self, cfg_path):
        self.global_config = GlobalConfig(cfg_path)
        self.plugin_imports = {}
        self.listener_list = {}
        self.data_manager = None

    def start(self):
        self.set_shutdown_hook()
        self.drop_permissions()
        self.global_config.read_config()
        self.data_manager = DataManager(self.global_config)
        self.data_manager.start()
        self.start_listeners()

    def drop_permissions(self):
        #
        # If we're not already root, don't bother dropping
        # permissions; authbind won't be able to bind low ports
        # anyway.
        #
        if os.getuid() != 0:
            return

        users_dict = {
            'centos': ('nobody', 'nobody'),
            'debian': ('nobody', 'nogroup')
        }
        dist_name = os.getenv('RECCE7_OS_DIST')
        if dist_name not in users_dict:
            return
        lowperm_user = users_dict[dist_name]

        nobody_uid = pwd.getpwnam(lowperm_user[0]).pw_uid
        nogroup_gid = grp.getgrnam(lowperm_user[1]).gr_gid

        os.setgroups([])

        os.setgid(nogroup_gid)
        os.setuid(nobody_uid)

        os.umask(0o077)

    def create_import_entry(self, port, name):
        imp = import_module('plugins.' + name)
        self.plugin_imports[port] = getattr(imp, name)

    def start_listeners(self):
        ports = self.global_config.get_ports()
        print("the ports are: " + str(ports))
        for port in ports:
            print("spawning this port:" + str(port))
            plugin_config = self.global_config.get_plugin_config(port)
            module = plugin_config['module']
            self.create_import_entry(port, module)
            listener = NetworkListener(plugin_config, self)
            listener.start()
            self.listener_list[port] = listener

    def set_shutdown_hook(self):
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, *args):
        print("Shutting down network listeners")
        for listener in self.listener_list.values():
            listener.shutdown()
        self.data_manager.shutdown()
        print("Goodbye.")

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
    :return: a reference to the plugin that was spawned
    '''
    def spawn(self, socket, config):
        # ToDo Throw exception if plugin class not found
        plugin_class = self.plugin_imports[config['port']]
        plugin = plugin_class(socket, self)
        plugin.start()
        return plugin

    '''
    Inserts the provided data into the data queue so that it can
    be pushed to the database.

    :param data: data object to add to the database
    '''
    def insert_data(self, data):
        self.data_manager.insert_data(data)

    def plugin_stopped(self, plugin):
        pass

#def main(cfg_path=None):
#    framework = Framework(cfg_path or default_cfg_path)
#    framework.start()

#if __name__ == '__main__': main()
