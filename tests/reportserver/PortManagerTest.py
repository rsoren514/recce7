import unittest

from common.GlobalConfig import Configuration

from reportserver.manager.PortManager import PortManager

# Unit tests for PortManager

class PortManagerTest(unittest.TestCase):

    def setUp(self):
        Configuration("./testconfig").getInstance()
        self.unit = PortManager()

    def test_setup_session_json(self):

        example_row = {'peerAddress': '127.0.0.1', 'user_input': 'hellow', 'session': 'f6cae8f0-5c61-4319-b357-1dcc20ab6fe4',
               'localAddress': '127.0.0.1', 'input_type': 'username', 'ID': 1, 'eventDateTime': '2016-04-23T16:12:20.497293'}

        expected_json = {
            'begin_time': '2016-04-23T16:12:20.497293',
            'end_time': '2016-04-23T16:12:20.497293',
            'local_address': '127.0.0.1',
            'peer_address': '127.0.0.1',
            'session': 'f6cae8f0-5c61-4319-b357-1dcc20ab6fe4'
         }

        json_received = self.unit.setup_session_json(example_row)

        self.assertEqual(json_received, expected_json)

    def test_get_date_delta(self):

        #one hour different
        test_iso_from = "1999-12-31T22:59:59"
        test_iso_to = "1999-12-31T23:59:59"
        expected_delta = "1:00:00"
        self.assertEqual(self.unit.get_date_delta(test_iso_from, test_iso_to), expected_delta)

        #the same
        test_iso_from = "1999-12-31T22:59:59"
        test_iso_to = "1999-12-31T22:59:59"
        expected_delta = "0:00:00"
        self.assertEqual(self.unit.get_date_delta(test_iso_from, test_iso_to), expected_delta)

        # seconds different
        test_iso_from = "1999-12-31T22:59:58"
        test_iso_to = "1999-12-31T22:59:59"
        expected_delta = "0:00:01"
        self.assertEqual(self.unit.get_date_delta(test_iso_from, test_iso_to), expected_delta)


    def test_process_port_data_one_row(self):

        example_results = [{'peerAddress': '127.0.0.1', 'user_input': 'hello',
                       'session': 'f6cae8f0-5c61-4319-b357-1dcc20ab6fe4',
                       'localAddress': '127.0.0.1', 'input_type': 'username', 'ID': 1,
                       'eventDateTime': '2016-04-23T16:12:20.497293'}]

        json_expected = {
                'begin_time': '2016-04-23T16:12:20.497293',
                'end_time': '2016-04-23T16:12:20.497293',
                'local_address': '127.0.0.1',
                'peer_address': '127.0.0.1',
                'session': 'f6cae8f0-5c61-4319-b357-1dcc20ab6fe4',
                'duration': '0:00:00',
                'session_items': [{
                    'peerAddress': '127.0.0.1',
                    'user_input': 'hello',
                    'session': 'f6cae8f0-5c61-4319-b357-1dcc20ab6fe4',
                    'localAddress': '127.0.0.1',
                    'input_type': 'username',
                    'ID': 1,
                    'eventDateTime': '2016-04-23T16:12:20.497293'
                }]
        }


        json_received = self.unit.process_port_data(example_results)


        print("expected:" + str(json_expected))
        print("received:" + str(json_received))

       # self.assertListEqual(json_received['session_items'], json_expected['session_items'])
        self.assertEqual(len(json_received), 1)
        self.assertEqual(json_received[0]['begin_time'], json_expected['begin_time'])
        self.assertEqual(json_received[0]['end_time'], json_expected['end_time'])
        self.assertEqual(len(json_received[0]['session_items']), 1)
        self.assertDictEqual(json_received[0]['session_items'][0], json_expected['session_items'][0])



if __name__ == "__main__":
    unittest.main()