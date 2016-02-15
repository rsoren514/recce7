import os
import unittest
from honeypot.src.database import DataQueue

#unit tests

'''This tests verifies that the data is inserted, that the queue is or
   is not empty at the appropriate time and that data is retrieved in the
   right order'''
class QueueTestCase(unittest.TestCase):

    def test_data_queue(self):
        q = DataQueue.dataQueue()
        list = ['ITEM1', 'ITEM2', 'ITEM3']
        list2 = ['ITEM4', 'ITEM5', 6, 7]
        q.insert_into_data_queue(list)
        q.insert_into_data_queue(list2)
        self.assertFalse(q.check_empty())
        self.assertEqual(q.get_next_item(),list)
        self.assertEqual(q.get_next_item(),list2)
        self.assertTrue(q.check_empty())


