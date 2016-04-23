import queue
from database import DataValidation

__author__ = 'Ben Phillips'


class DataQueue:

    def __init__(self, global_config):
        self.dataQueue = queue.Queue()
        self.dv = DataValidation.DataValidation(global_config)
    """we want to check the data here and fail early
        if the data is good then we want to put it in the data queue
        we will want another python script for the validations (DataValidation.py)
        we need to enforce type constraints because the database will not
        see DataValidation.py"""
    def insert_into_data_queue(self, value):

        if self.dv.run_all_checks(value):
            self.dataQueue.put(value)
            return True
        else:
            return False

    @staticmethod
    def get_data_validator(self):
        return self.dv

    def get_next_item(self):
        item = self.dataQueue.get()
        self.dataQueue.task_done()
        return item

    def check_empty(self):
        result = self.dataQueue.empty()
        return result
