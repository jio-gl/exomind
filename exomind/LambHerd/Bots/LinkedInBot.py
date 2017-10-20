from exomind.Attributes import *
from exomind.ExomindException import BotException
from SandMan import SandMan

from mechanize import Browser
import urllib2
import mechanize
import urllib2, urllib
import re, time
import sys, traceback

from threading import Lock

class Link:
    pass

class LinkedInBot:
    
    __regex = 'href="/profile[a-zA-Z0-9?&_=\-%]+" class="fn" title="[a-zA-Z\' ]+">[a-zA-Z\' ]+<'
    __regex2 = 'href="http://www.linkedin.com/profile[a-zA-Z0-9?&_=\-%]+" ><strong class="fn">[a-zA-Z\' ]+<'
    __complete_name_regex = '>[a-zA-Z\' ]+<'
    __complete_name_prefix = '>'
    __complete_name_sufix = '<'

    __url_regex = '/profile[a-zA-Z0-9?&_=\-%]+'
    __url_prefix = ''
    __url_sufix = ''

    def __init__(self):
        pass

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        
        print 'INIT: LinkedInBot'
        
        self.__br = Browser()
        self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(debug)
        self.__sandman = SandMan('LinkedInBot')
        self.__debug = debug

        # sign in
        
        try:
            self.__br.open("https://www.linkedin.com/secure/login?trk=hb_signin")
            self.__br.select_form(nr=1)
            self.__br['session_key'] = user
            self.__br['session_password'] = passw
            resp = self.__br.submit()
            resp = self.__br.open('http://www.linkedin.com/home')
            self.__good = True
        except Exception, e:
            if self.__debug:
                traceback.print_exc(file=sys.stdout)
            print 'Exception on LinkedInBot, possibly bad user/password or https login don\' work behind a proxy.'
            self.__good = False

        self.__lock = Lock()


    def set_proxies_per_proto(self, proxies):
        self.__br.set_proxies(proxies)       

    def set_sleep_secs(self, secs):
        self.__sandman.set_sleep_secs(secs)        

    def set_sleep_module(self, iterations):
        self.__sandman.set_sleep_module(iterations)        

    def set_sleep_failure(self, secs):
        self.__sandman.set_sleep_failure(secs)

    def set_sleep_random_flag(self, bool):
        self.__sandman.set_sleep_random_flag(bool)

    def search(self, query):
        self.__sandman.try_to_sleep()        
        print '(LinkedInBot) searching...'
        link = Link()
        url_query = urllib.urlencode({'kwname':query})
        link.absolute_url = 'http://www.linkedin.com/search?search=&sortCriteria=4&rd=out&' + url_query
        resp = self.__br.follow_link(link)
        cont = resp.read()
        links = re.findall('http://www.linkedin.com/profile?[a-zA-Z0-9?&_=\-%]+', cont)        
        # remove repetitions
        links = list(set(links))
        
        links_urls = []
        for link in links:
            links_urls.append(link)
        return links_urls

    def __strip_complete_name(self, html_match):
        match = re.search(self.__complete_name_regex, html_match)
        match = match.group()[len(self.__complete_name_prefix):-len(self.__complete_name_sufix)]
        return match

    def __strip_url(self, html_match):
        match = re.search(self.__url_regex, html_match)
        match = match.group()[len(self.__url_prefix):]
        return 'http://www.linkedin.com' + match

    def also_viewed(self, (names, graph)):
        self.__sandman.try_to_sleep()        
        if not self.__good:
            print 'EXCEPTION on LinkedInBot, possibly https login don\' work behind a proxy.'
            return [], {}, {}
        self.__lock.acquire()
        try:
            return self.__impl_recommends(names, 'also_view')
        finally:
            self.__lock.release() # release lock, no matter what        

    def recommendations(self, (names, graph)):
        self.__sandman.try_to_sleep()        
        if not self.__good:
            print 'EXCEPTION on LinkedInBot, possibly https login don\' work behind a proxy.'
            return [], {}, {}
        self.__lock.acquire()
        try:
            return self.__impl_recommends(names, 'recomm')
        finally:
            self.__lock.release() # release lock, no matter what        

    def __impl_recommends(self, names, type='recomm'):
        # make it a list if is only a string
        if str(names) == names:
            names = [names]
        br = self.__br
        # check if name exists.
        for name in names:
            results = self.search(name)
            if len(results) != 0:
                break
        # assume the first person that matches
        if len(results) == 0:
            return [], {}, {}
        name_link = results[0]
        # retrieve the first n (50?) contacts as tuples (complete_name, linkedin_url).
        full_url = name_link # + ('/%s' % type)
        # only view Recommendations
        if type == 'recomm':
            full_url = full_url.replace('viewProfile', 'viewRecs')
            resp = self.__br.open(full_url )
            cont = resp.read()
            matches = re.findall(self.__regex, cont)
        else: # also view
            resp = self.__br.open(full_url )
            cont =  resp.read()
            m = re.search('items\?p=[A-Za-z0-9]+\'', cont)
            if not m:
                return [], {}, {}
            p = m.group()[len('items?p='):-1]
            url_query = urllib.urlencode({'p':p})
            link = Link()
            link.absolute_url = 'http://www.linkedin.com/ape-delivery/items?' + url_query
            resp = self.__br.follow_link(link)
            cont = resp.read()
            matches = re.findall(self.__regex2, cont)
            
        complete_names = map(self.__strip_complete_name, matches)            
        urls = map(self.__strip_url, matches)    
        
        self_attrs, node_dict, link_dict = [], {}, {}
        for name, url in zip(complete_names, urls):
            node_dict[name] = []
            node_dict[name] += [(Attributes.URL_SOURCE_ATTR,url)]
            node_dict[name] += [(Attributes.ALIAS_ATTR,name)]
            node_dict[name] += [(Attributes.LINKEDIN_ALIAS_ATTR,name)]                                    
            link_dict[name] = [(Attributes.URL_SOURCE_ATTR,full_url)]
        return self_attrs, node_dict, link_dict

    def is_chatbot(self):
        return False

    def save_cache(self):
        pass



if __name__=='__main__':

    pass



