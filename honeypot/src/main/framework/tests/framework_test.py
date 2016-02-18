__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import unittest
from framework.frmwork import Framework
from unittest.mock import patch

config_path = '/tests/testConfig.cfg'


class FrameworkTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('networklistener.NetworkListener.start')
    def test_plugins_enabled(self, test_patch):
        framework = Framework(config_path)
        expected = {
            8082: {
                'port': 8082,
                'module': 'HTTPPlugin',
                'table': 'test',
                'enabled': 'Yes',
                'tableColumns': [[1, 'INTEGER', 'someNumber'], [2, 'TEXT', 'someText']]
            }
        }
        self.assertEqual(expected, framework.config_dictionary)
        self.assertTrue(test_patch.called)
        self.assertEquals(1, test_patch.call_count)

    @patch('networklistener.NetworkListener.start')
    def test_plugins_disabled(self, test_patch):
        framework = Framework(config_path)
        self.assertTrue(8083 not in framework.config_dictionary)
        self.assertTrue(8082 in framework.config_dictionary)
        self.assertEquals(1, test_patch.call_count)

    @patch('networklistener.NetworkListener.start')
    def test_get_config(self, test_patch):
        framework = Framework(config_path)
        expected = {
            'port': 8082,
            'module': 'HTTPPlugin',
            'table': 'test',
            'enabled': 'Yes',
            'tableColumns': [[1, 'INTEGER', 'someNumber'], [2, 'TEXT', 'someText']]
        }
        self.assertEqual(expected, framework.get_config(8082))

    @patch('networklistener.NetworkListener.start')
    @patch('plugins.HTTPPlugin.HTTPPlugin.start')
    def test_spawn(self, net_patch, plugin_patch):
        framework = Framework(config_path)
        framework.spawn(None, {'port': 8082})
        self.assertTrue(plugin_patch.called)

    def tearDown(self):
        pass