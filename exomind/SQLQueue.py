
from ExomindException import ExomindException
from Utils import normalize_token

class SQLQueue:
    
    def __init__(self, name, builder_rep=None):
        if not builder_rep:
            raise ExomindException('you cannot create SQLQueue instances, use QueueBuilder instead')
        self.__name = name
        self.__rep = builder_rep

    def __len__(self):
        return self.__rep.len(self.__name)
        
    def elems(self):
        return self.__rep.get_elems(self.__name)
        
    def push(self, n):
        n = normalize_token(n)
        self.__rep.push(self.__name, n)
        
    def pop(self, type='LIFO'):
        return self.__rep.pop(self.__name, type)
        
    def unpop(self, n, type='LIFO'):
        n = normalize_token(n)
        return self.__rep.unpop(self.__name, n, type)
        
    def __contains__(self, n):
        n = normalize_token(n)
        return self.__rep.exists_elem(self.__name, n)
    
    def drop(self):
        self.__rep.drop_queue(self.__name)