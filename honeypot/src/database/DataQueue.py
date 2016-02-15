import queue

class dataQueue:

    dataQueue = queue.Queue()

    def insert_into_data_queue(cls,value):
        cls.dataQueue.put(value)

    def get_next_item(cls):
        item = cls.dataQueue.get()
        cls.dataQueue.task_done()
        return item

    def check_empty(cls):
        result = cls.dataQueue.empty()
        return result
