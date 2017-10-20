
"""
Based On
http://codemagnet.blogspot.com/2008/07/python-fun-project-msn-chat-bot.html
Marcus Low of malaysia :
"""

import msnlib
import msncb

from ChatBot import ChatBot 
from MSNBotCallBacks import *

from mechanize import Browser
import mechanize
import urllib2, urllib
import re, time
from time import gmtime, strftime
import os.path

# time, for sleeping (see last line)
import time
# select to wait for events
import select
# socket, to catch errors
import socket
import string
import sys
import urllib


from threading import Lock




class MSNBot:

    def is_chatbot(self):
        return True

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        
#        print 'INIT: MSNBot'
        self.__proxies = proxies_per_proto
        self.__user = user
        self.__pass = passw
        self.__debug = debug
        
        self.recipient_list = []        

    def set_proxies_per_proto(self, proxies):
        self.__proxies = proxies

    def set_sleep_failure(self, secs):
        self.__sleep_failure = float(secs)        

    def set_sleep_secs(self, secs):
        self.__sleep_secs = secs

    def set_sleep_module(self, iterations):
        self.__sleep_module = iterations

    def set_sleep_random_flag(self, bool):
        self.__sleep_random_flag = bool        

    def set_debug(self, debug):
        self.__debug = debug

    def set_bot_globals(self):
        # global variables
        self.m.glob_history_ring = []    # history buffer
        self.m.glob_last_sent = ''        # email of the last person we sent a message to
        self.m.glob_last_received = ''    # email of the last person we received a message from
        self.m.glob_ignored = []        # people being locally ignored
        
        # auto-away
        self.m.glob_timeout = None        # must be None, not 0 because of select() semantics
        self.m.glob_auto_away = 0
        
        self.m.glob_config = {}
        self.m.glob_config['history directory'] = os.path.expanduser('~') + "/.exomind/msnbot"
        self.m.glob_config['history directory2'] = "."
        self.m.glob_config['history size'] = 100000
        
        self.m.auto_responses = None
        self.m.chatbot_type = 'se' # or 'eliza'
        
    def connect(self, nick=None, query_for_distances=True, voc_translator=None):
               
        self.nick = nick
        
        self.m = msnlib.msnd(self.__debug)
        self.m.cb = msncb.cb()        
        self.m.sebot = ChatBot(self.__proxies, query_for_distances)
        self.m.sebot.set_voc_translator(voc_translator)

        self.m.email = self.__user
        self.m.pwd = self.__pass
        
        print "(MSNBot) Logging In"
        try:
            self.m.login()
            print "(MSNBot) Logging Finished!"
        except:
            raise Exception('Login failed at MSNBot instance! connect()')

        self.set_bot_globals()

        print "Sync"
        # this makes the server send you the contact list, and it's recommended that
        # you do it because you can get in trouble when getting certain events from
        # people that are not on your list; and it's not that expensive anyway
        self.m.sync()

        print "Changing Status to online %s" % self.m.email
        # any non-offline status will do, otherwise we'll get an error from msn when
        # sending a message
        self.m.change_status("online")
        self.m.change_nick(self.nick)
        
        auto_responses = None

        # SET CALLBACKS!    
        self.m.cb.add = cb_add
        self.m.cb.msg = cb_msg

    def set_first_input (self, recipient_list, initial_msg_list, repeat_in_secs = 3600) :
        
        self.bak_recipient_list = recipient_list
        self.bak_initial_msg_list = initial_msg_list
        
        self.m.initial_time = time.time()
        self.__repeat_in_secs= repeat_in_secs
        self.__first_initial_sent = False

    def start_chatting(self, all_auto=False):
        
        # we loop over the network socket to get events
        print "Start Chatting! Loop..."
        
        icount = 0
        self.m.glob_quit = False
        while self.m.glob_quit == False:
            
            # we get pollable fds
            t = self.m.pollable()
            infd = t[0]
            outfd = t[1]    
            
            # we select, waiting for events
            fds = select.select(infd, outfd, [], 0)
            
            icount += 1        
            
            # first message
            if not self.__first_initial_sent and int(time.time()) - int(self.m.initial_time) > 5:
                self.recipient_list = self.bak_recipient_list
                self.initial_msg_list = self.bak_initial_msg_list
                self.__first_initial_sent = True
                
            if int(time.time()) % self.__repeat_in_secs == 0: 
            #if (icount % 500 == 0 ) :
                self.recipient_list = self.bak_recipient_list
                self.initial_msg_list = self.bak_initial_msg_list 
                time.sleep(1.0)               
        
            for i in fds[0] + fds[1]:    # see msnlib.msnd.pollable.__doc__
                try:
                    self.m.read(i)            
                    if (self.recipient_list != [] and not 'quit' in self.recipient_list) :
                        for recipient, msg in zip(self.recipient_list, self.initial_msg_list):
                            tim = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
                            print '(MSNBot) %s >>> %s (INITIAL MSG): %s' % (tim, recipient, msg)
                            self.m.sendmsg(recipient, msg)
                        self.recipient_list = []
                        self.initial_msg_list = []
                        
                    if ('quit' in self.recipient_list) :
                        self.m.close(i)                
                    
                except ('SocketError', socket.error), err:
                    if i != self.m:
                        # user closed a connection
                        # note that messages can be lost here
                        self.m.close(i)
                    else:
                        # main socket closed
                        quit(1)
            
            # sleep a bit so we don't take over the cpu
            time.sleep(0.01)
        
    def is_msn_email(self, email):
        domain = email.split('@')[1]
        good = [
                'hotmail.com',
                'live.com',
                'msn.com'
                ]
        for good_d in good:
            if good_d in domain:
                return True
        return False
        
    def add_contact(self, msn_mail):
        self.m.useradd(msn_mail)
    
    def save_cache(self):
        pass


    
if __name__ == '__main__':
    
    bot = MSNBot()
    bot.initialize({}, "blabla@live.com.ar", "blabla")
    bot.connect('BOTO', False)
    bot.set_first_input(['bloblo@hotmail.com'], ['hello'])    
    bot.start_chatting()
