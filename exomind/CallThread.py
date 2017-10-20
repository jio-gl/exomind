
# thread imports
from threading import Thread

class CallThread(Thread):
    
   def __init__ (self, function, param):
       Thread.__init__(self)
       self.status = -1
       self.function = function
       self.param = param
       self.ret_val = None
       self.exception = None
      
   def run(self):
       self.ret_val = self.function(self.param)
            



   
        
