from threading import Thread, Condition
from honeypot.src.database import DataQueue, DB_Init


class DataManager():

    def __init__(self):
        self.q = DataQueue.dataQueue()
        self.condition = Condition()
        self.CThread(self.condition, self.q).start()
        DB_Init.create_default_database()

    class CThread(Thread):
        '''over ride run method'''
        def __init__(self, condition_ref, q_ref):
            Thread.__init__(self)
            self.condition = condition_ref
            self.q = q_ref

        def run(self):
            '''loop forever'''
            while True:
                '''get lock'''
                self.condition.acquire()
                '''if the q is empty'''
                if self.q.check_empty():
                    '''release the lock and wait'''
                    self.condition.wait()
                '''otherwise get the value off the queue'''
                value = self.q.get_next_item()
                '''set task_done (need to research this)'''
                #self.q.task_done()
                '''print value consumed'''
                print("Consumed :", value)
                '''we have the lock acquired so we can notify'''
                self.condition.notify()
                '''we release the lock so that the notified threads can resume'''
                self.condition.release()

    def insert_data(self, data):
        self.condition.acquire()
        self.q.insert_into_data_queue(data)
        self.condition.notify()
        self.condition.release()










