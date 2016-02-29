__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import os
import unittest
from framework.frmwork import Framework, main
from unittest.mock import patch

config_path = '/tests/testConfig.cfg'


def make_mock_config(port, module):
    return {
        'port': port,
        'module': module,
        'table': 'test',
        'enabled': 'Yes',
        'tableColumns': [[1, 'INTEGER', 'someNumber'], [2, 'TEXT', 'someText']]
    }


class FrameworkTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('networklistener.NetworkListener.start')
    def test_plugins_enabled(self, test_patch):
        framework = Framework(config_path)
        framework.start()
        expected = {
            8082: make_mock_config(8082, 'HTTPPlugin')
        }
        self.assertEqual(expected, framework.global_config.config_dictionary)
        self.assertTrue(test_patch.called)
        self.assertEquals(1, test_patch.call_count)

    @patch('networklistener.NetworkListener.start')
    def test_plugins_disabled(self, test_patch):
        framework = Framework(config_path)
        framework.start()
        self.assertTrue(8083 not in framework.global_config.config_dictionary)
        self.assertTrue(8082 in framework.global_config.config_dictionary)
        self.assertEquals(1, test_patch.call_count)

    @patch('networklistener.NetworkListener.start')
    def test_get_config(self, test_patch):
        framework = Framework(config_path)
        framework.start()
        expected = make_mock_config(8082, 'HTTPPlugin')
        self.assertEqual(expected, framework.get_config(8082))

    @patch('networklistener.NetworkListener.start')
    @patch('plugins.HTTPPlugin.HTTPPlugin.start')
    def test_spawn(self, net_patch, plugin_patch):
        framework = Framework(config_path)
        framework.start()
        framework.spawn(None, {'port': 8082})
        self.assertTrue(plugin_patch.called)

    @patch.object(Framework, 'start')
    def test_main(self, mock_framework_start):
        main()
        self.assertTrue(mock_framework_start.called)

    def test_get_db_path(self):
        fw = Framework(config_path)
        self.assertEqual(fw.global_config.get_db_path(),
                         os.getenv('HOME') + '/honeyDB/honeyDB.sqlite')

    def tearDown(self):
        pass