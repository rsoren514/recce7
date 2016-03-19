__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import os
import unittest
from framework.frmwork import Framework
from unittest.mock import patch
from unittest.mock import MagicMock
from database.DataManager import DataManager
from plugins.HTTPPlugin import HTTPPlugin
import pwd
import grp
import socket


config_path = '/tests/testConfig.cfg'


def make_mock_config(port, module):
    return {
        'port': port,
        'module': module,
        'table': 'test',
        'enabled': 'Yes',
        'rawSocket': 'No',
        'tableColumns': [[1,'someNumber','INTEGER'], [2,'someText','TEXT']]
    }


class FrameworkTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_plugins_enabled(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        expected = {
            8082: make_mock_config(8082, 'HTTPPlugin')
        }
        self.assertEqual(expected, framework.global_config.config_dictionary)
        self.assertEquals(1, mock_nl_start.call_count)
        self.assertTrue(mock_dm_start.called)

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_plugins_disabled(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        self.assertTrue(8083 not in framework.global_config.config_dictionary)
        self.assertTrue(8082 in framework.global_config.config_dictionary)
        self.assertEquals(1, mock_nl_start.call_count)

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_get_config(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        expected = make_mock_config(8082, 'HTTPPlugin')
        self.assertEqual(expected, framework.get_config(8082))

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    @patch.object(socket.socket, 'getsockname', return_value='0.0.0.0')
    @patch.object(socket.socket, 'getpeername', return_value='0.0.0.1')
    def test_spawn(self, mock_gpn, mock_gsn, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        with patch('plugins.HTTPPlugin.HTTPPlugin.start') as mock_http_start:
            framework.spawn(socket.socket(), {'port': 8082})
        self.assertTrue(mock_http_start.called)

#    @patch.object(Framework, 'start')
#    def test_main(self, mock_framework_start):
#        main()
#        self.assertTrue(mock_framework_start.called)

    def test_get_db_dir(self):
        fw = Framework(config_path)
        self.assertEqual(fw.global_config.get_db_dir(),
                         os.getenv('HOME') + '/honeyDB')

    def get_current_umask(self):
        # Python has no way to obtain the current umask without
        # changing it, so we do this hooptiness...
        old_umask = os.umask(0)
        os.umask(old_umask)
        return old_umask

    def test_drop_permissions(self):
        fw = Framework(config_path)

        nobody_uid = pwd.getpwnam('nobody').pw_uid
        nogroup_gid = grp.getgrnam('nogroup').gr_gid

        with patch('os.getuid', return_value=0) as mock_get_uid:
            with patch('os.setgroups') as mock_setgroups:
                with patch('os.setuid') as mock_setuid:
                    with patch('os.setgid') as mock_setgid:
                        fw.drop_permissions()
        mock_setuid.assert_called_with(nobody_uid)
        mock_setgid.assert_called_with(nogroup_gid)
        mock_setgroups.assert_called_with([])

    def test_dont_drop_permissions(self):
        fw = Framework(config_path)

        with patch('os.setgroups') as mock_setgroups:
            with patch('os.setuid') as mock_setuid:
                with patch('os.setgid') as mock_setgid:
                    fw.drop_permissions()
        self.assertFalse(mock_setuid.called)
        self.assertFalse(mock_setgid.called)
        self.assertFalse(mock_setgroups.called)

    @patch('database.DataManager.DataManager.start', return_value=None)
    @patch('framework.networklistener.NetworkListener.start')
    def test_insert_data(self, mock_nl_start, mock_dm_start):
        fw = Framework(config_path)
        fw.start()
        test_dict = {'a': 1, 'b': 2}
        with patch('database.DataManager.DataManager.insert_data') as mock_insert_data:
            fw.insert_data(test_dict)
            mock_insert_data.assert_called_with(test_dict)

    def tearDown(self):
        pass