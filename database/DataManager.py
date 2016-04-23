from common.logger import Logger
from threading import Thread, Condition
from database import DataQueue, Table_Insert
from database.DB_Init import Database

__author__ = 'Ben Phillips'

'''we will need threading and a condition variable for synchronization
This is the DataManager class, it creates the database, data queue and
the condition variable for synchronization between it, the framework and
the plugins'''


class DataManager(Thread):

    def __init__(self, global_config):
        super().__init__()
        self.db = Database(global_config)
        self.db.create_default_database()
        self.q = DataQueue.DataQueue(global_config)
        self.condition = Condition()
        self.kill = False
        self.logger = Logger().get('database.DataManager.DataManager')

    '''Overriding the thread run method. This will insert all data
    in the queue and then once finished give up control of the
    condition variable'''
    def run(self):
        """loop forever"""
        while not self.kill:
            self.condition.acquire()
            if self.q.check_empty():
                '''if empty pass off control of the condition variable'''
                self.condition.wait()

            while not self.q.check_empty():
                value = self.q.get_next_item()
                Table_Insert.prepare_data_for_insertion(
                    self.q.dv.table_schema, value)
                '''we have the lock acquired so we can notify'''
                self.condition.notify()

            '''we release the lock so that the notified threads can resume'''
            self.condition.release()

    '''called by plugin, we check the data against the database before insert
    into queue. If the data is bad we do not put on queue and therefor
    do not notify consumer.'''
    '''TODO Will want to provide meaningful errors to plugin author'''
    def insert_data(self, data):
        self.condition.acquire()
        if self.q.insert_into_data_queue(data):
            self.condition.notify()
            self.condition.release()
        else:
            self.condition.release()

    def shutdown(self):
        self.kill = True
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
        self.join()
        self.logger.debug('Data manager has shut down.')

    def check_kill_status(self):
        return self.kill
