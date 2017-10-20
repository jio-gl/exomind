
import random, time, sys

class SandMan:
    
    def __init__(self, callername):
        self.__sleep_secs = 0.0
        self.__sleep_random_flag = False
        self.__sleep_module = 9999999
        self.__gets = 0
        self.__name = callername
    
    def set_sleep_secs(self, secs):
        self.__sleep_secs = float(secs)

    def set_sleep_module(self, iterations):
        self.__sleep_module = iterations

    def set_sleep_random_flag(self, bool):
        self.__sleep_random_flag = bool        
    
    def __unautomate(self):
        print 'Press Enter to continue:'
        sys.stdin.readline()
    
    def try_to_sleep(self):
        # DON'T UNCOMMENT THE FOLLOWING LINE!!!
        # OTHERWISE YOU WILL PROBABLY BE VIOLATING SOME USER AGREEMENT OR TERM OF USE.
        #self.__unautomate()
        print 'Bot operations count --> %d' % self.__gets
        self.__gets += 1        
        if self.__gets % self.__sleep_module == 0:
            if self.__sleep_random_flag:
                sleep_time = random.random() * self.__sleep_secs * 2.0
                print '(%s) Sleeping for random seconds between [0.0, %.1f], every %d Bot operations' % (self.__name, self.__sleep_secs*2, self.__sleep_module)                
            else:
                sleep_time = self.__sleep_secs
                print '(%s) Sleeping for %f seconds, every %d Bot operations' % (self.__name, self.__sleep_secs, self.__sleep_module)            
            time.sleep(sleep_time)            
        
