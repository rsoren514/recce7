import queue
from honeypot.src.database import DataValidation

class dataQueue:

    def __init__(self):
        self.dataQueue = queue.Queue()
        self.dv = DataValidation.DataValidation()

    def insert_into_data_queue(self,value):
        #we want to check the data here and fail early
        #if the data is good then we want to put it in the data queue
        #we will want another python script for the validations (DataValidation.py)
        #we need to enforce type constraints because the database will not
        #see DataValidation.py
        if self.dv.run_all_checks(value):
            self.dataQueue.put(value)
            return True
        else:
            return False


    def get_next_item(self):
        item = self.dataQueue.get()
        self.dataQueue.task_done()
        return item

    def check_empty(self):
        result = self.dataQueue.empty()
        return result
