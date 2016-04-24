import socket
import unittest

from framework.frmwork import Framework
from framework.networklistener import NetworkListener
from unittest.mock import Mock
from unittest.mock import patch

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

config_path = 'tests/framework/testConfig.cfg'


def make_mock_config(port, module, clsname):
    return {
        'port': port,
        'table': 'test',
        'module': module,
        'moduleClass': clsname,
        'enabled': 'Yes',
        'rawSocket': 'No',
        'tableColumns': [
            [1, 'someNumber', 'INTEGER'],
            [2, 'someText', 'TEXT']
        ]
    }


class NetworkListenerTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('framework.networklistener.NetworkListener.start_listening')
    def test_plugins_enabled(self, mock_start_listening):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        listener = NetworkListener('', mock_config, None)
        listener.start()
        while listener.connection_count == 0:
            pass
        listener._session_socket = None
        listener.shutdown()
        self.assertTrue(mock_start_listening.called)

    def test_connection_count(self):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        listener = NetworkListener('', mock_config, None)
        self.assertEqual(0, listener.connection_count)
        listener.connection_count = 5
        self.assertEqual(5, listener.connection_count)

    @patch.object(Framework._Framework, 'spawn')
    def test_start_listening(self, mock_framework):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        with patch('framework.networklistener.socket.socket.accept') \
                as mock_accept:
            mock_accept.return_value = (socket.socket(), '192.168.1.1')
            listener = NetworkListener('', mock_config, mock_framework)
            listener._running = True
            skt = socket.socket()
            listener.start_listening(skt)
            skt.close()
        self.assertTrue(mock_accept.called)
        self.assertTrue(mock_framework.spawn.called)

    @patch.object(Framework._Framework, 'spawn')
    def test_start_listening_exception(self, mock_framework):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        mock_socket = Mock()
        mock_socket.accept = Mock()
        mock_socket.accept.side_effect = Exception(
            '(this error is expected)')
        listener = NetworkListener('', mock_config, None)
        self.assertRaises(Exception, listener.start_listening, mock_socket)

    @patch.object(Framework._Framework, 'spawn')
    def test_start_listening_oserror(self, mock_framework):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        mock_socket = Mock()
        mock_socket.accept = Mock()
        mock_socket.accept.side_effect = OSError()
        mock_socket.accept.side_effect.errno = 22
        listener = NetworkListener('', mock_config, mock_socket)
        try:
            listener.start_listening(mock_socket)
        except OSError:
            self.fail('OSError should be handled when errno == 22.')

        mock_socket.accept.side_effect.errno = 0
        self.assertRaises(OSError, listener.start_listening, mock_socket)

    @patch.object(Framework._Framework, 'spawn')
    def test_start_listening_connection_aborted(self, mock_framework):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        mock_socket = Mock()
        mock_socket.accept = Mock()
        mock_socket.accept.side_effect = ConnectionAbortedError
        listener = NetworkListener('', mock_config, mock_socket)
        listener._running = True
        self.assertRaises(ConnectionAbortedError,
                          listener.start_listening,
                          mock_socket)
        listener._running = False
        try:
            listener.start_listening(mock_socket)
        except ConnectionAbortedError:
            self.fail('ConnectionAbortedError should be handled when listener '
                      'is not running.')

    @patch('framework.networklistener.NetworkListener.join')
    def test_nl_shutdown(self, mock_join):
        mock_config = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        mock_socket = Mock()
        mock_socket.shutdown = Mock()
        mock_socket.detach = Mock()
        mock_socket.close = Mock()
        listener = NetworkListener('', mock_config, None)
        listener._session_socket = mock_socket
        listener._running = True

        with patch('platform.system', return_value='Darwin'):
            listener.shutdown()
        self.assertFalse(listener._running)
        self.assertTrue(mock_socket.close.called)
        self.assertTrue(mock_join.called)

        listener.running = True
        with patch('platform.system', return_value='Linux'):
            listener.shutdown()
        self.assertFalse(listener._running)
        self.assertTrue(mock_socket.shutdown.called)
        self.assertEqual(2, mock_join.call_count)

        listener._session_socket = None
        listener.running = True
        with patch('platform.system', return_value='Linux') as mock_system:
            listener.shutdown()
        self.assertFalse(listener._running)
        self.assertFalse(mock_system.called)
        self.assertEqual(3, mock_join.call_count)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()