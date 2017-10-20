
from CallThread import *

class CallBatch:
    
    def __init__(self, functions, params, threads=8):
        self.__funs = functions
        self.__params = params
        self.__threads = threads        
        
    def run(self):

       ret_vals = {}
       threads = self.__threads

       partial = 0
       while partial < len(self.__funs):

           threadlist = []
           thread_count = 0
           while thread_count < threads and partial < len(self.__funs):               
               current = CallThread(self.__funs[partial], self.__params[partial])
               threadlist.append(current)
               current.start()
               partial += 1
               thread_count += 1

           for thread in threadlist:
               thread.join()
               if thread.exception:
                   raise thread.exception
               ret_vals[(thread.function, '|'.join(thread.param[0]))] = thread.ret_val

       return ret_vals
