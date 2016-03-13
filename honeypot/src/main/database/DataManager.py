__author__ = 'Ben Phillips'

'''we will need threading and a condition variable for synchronization'''
from threading import Thread, Condition
from database import DataQueue, DB_Init, Table_Insert

'''This is the DataManager class, it creates the database, data queue and
the condition variable for synchronization between it, the framework and
the plugins'''
class DataManager():

    def __init__(self,global_config_instance):
        DB_Init.create_default_database(global_config_instance)
        self.q = DataQueue.dataQueue(global_config_instance)
        self.condition = Condition()
        self.CThread(self.condition, self.q).start()

    '''This thread is the consumer thread that pulls from the FIFO queue'''
    class CThread(Thread):
        '''I give this thread a reference to the condition variable
        and the data queue'''
        def __init__(self, condition_ref, q_ref):
            Thread.__init__(self)
            self.condition = condition_ref
            self.q = q_ref

        '''Overriding the thread run method. This will insert all data
        in the queue and then once finished give up control of the
        condition variable'''
        def run(self):
            '''loop forever'''
            while True:
                self.condition.acquire()
                if self.q.check_empty():
                    '''if empty pass off control of the condition variable'''
                    self.condition.wait()
                value = self.q.get_next_item()
                Table_Insert.prepare_data_for_insertion(self.q.dv.table_schema, value)
                '''we have the lock acquired so we can notify'''
                self.condition.notify()
                '''we release the lock so that the notified threads can resume'''
                self.condition.release()

    '''called by plugin, we check the data against the database before insert
    into queue. If the data is bad we do not put on queue and therefor
    do not notify consumer.'''
    #TODO Will want to provide meaningful errors to plugin author
    def insert_data(self, data):
        self.condition.acquire()
        if self.q.insert_into_data_queue(data):
            self.condition.notify()
            self.condition.release()
        else:
            self.condition.release()










