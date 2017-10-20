
from QueueBuilderRep import QueueBuilderRep
from SQLQueue import SQLQueue

class QueueBuilder:
    
    def __init__(self, db_user, db_passwd):
        self.__rep = QueueBuilderRep(db_user, db_passwd)
        
    def __contains__(self, queue_name):
        return queue_name in self.__rep
    
    def __create_queue(self, queue_name, create_index):
        self.__rep.create_queue(queue_name, create_index)
        
    def drop_queue(self, queue_name):
        self.__rep.drop_queue(queue_name)
        
    def get_queue(self, queue_name, drop_if_exists=True, create_index=False):
        if not queue_name in self:
            self.__create_queue(queue_name, create_index)
        else:
            if drop_if_exists:
                self.drop_queue(queue_name)
                self.__create_queue(queue_name, create_index)
        return SQLQueue(queue_name, self.__rep)
    
    def __iter__(self):
        return self.__rep.get_Queues(False)