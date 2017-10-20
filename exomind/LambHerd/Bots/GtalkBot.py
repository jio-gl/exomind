

from exomind.Attributes import *
from exomind.ExomindException import BotException

from mechanize import Browser
import mechanize
import urllib2, urllib
import re, time


from threading import Lock

class GtalkBot:
    
    def is_chatbot(self):
        return True

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        
        #print 'INIT: GTalkBot (not implemented)'
        pass

    def set_proxies_per_proto(self, proxies):
        pass

    def set_sleep_failure(self, secs):
        self.__sleep_failure = float(secs)        

    def set_sleep_secs(self, secs):
        self.__sleep_secs = secs

    def set_sleep_module(self, iterations):
        self.__sleep_module = iterations

    def set_sleep_random_flag(self, bool):
        self.__sleep_random_flag = bool        

    def save_cache(self):
        pass



