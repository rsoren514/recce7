import queue
from honeypot.src.database import DataValidation

class dataQueue:

    dataQueue = queue.Queue()
    dv = DataValidation.DataValidation()

    def insert_into_data_queue(cls,value):
        #we want to check the data here and fail early
        #if the data is good then we want to put it in the data queue
        #we will want another python script for the validations (DataValidation.py)
        #we need to enforce type constraints because the database will not
        #see DataValidation.py
        if cls.dv.run_all_checks(value):
            cls.dataQueue.put(value)
            return True
        else:
            return False


    def get_next_item(cls):
        item = cls.dataQueue.get()
        cls.dataQueue.task_done()
        return item

    def check_empty(cls):
        result = cls.dataQueue.empty()
        return result
