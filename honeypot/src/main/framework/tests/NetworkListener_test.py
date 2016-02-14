__author__ = 'jessenelson'

import unittest
from main.framework.framework import NetworkListener
from unittest.mock import patch

class NetworkListenerTest(unittest.TestCase):
    def setUp(self):
        pass

    # @patch('main.framework.framework.Framework.spawn')
    @patch('main.framework.networklistener.NetworkListener.start_listening')
    # @patch('main.framework.NetworkListener.socket.socket.accept')
    def test_plugins_enabled(self, test_framework):
        mock_config = {
            'port': 8082,
            'module': 'HTTPPlugin',
            'table': 'test',
            'enabled': 'Yes',
            'tableColumns': [[1, 'INTEGER', 'someNumber'], [2, 'TEXT', 'someText']]
        }
        listener = NetworkListener(mock_config, test_framework)
        listener.start()
