from exomind.Attributes import *
from exomind.ExomindException import BotException
from SandMan import SandMan

from mechanize import Browser
import mechanize
import urllib2, urllib
import re, time


from threading import Lock

class Link:
    absolute_url = None

class FacebookBot:
    
    __regex = '<span class=\\\\"fname\\\\">[a-zA-Z0-9\\-_ .]+<\\\\/span><div class=\\\\"flinks\\\\"><a href=\\\\"\\\\/inbox\\\\/\?compose&amp;id=[0-9]+\\\\">'
    __complete_name_regex = '<span class=\\\\"fname\\\\">[a-zA-Z0-9\\-_ .]+<\\\\/span>'    
    __complete_name_prefix = '<span class=\\"fname\\">'
    __complete_name_sufix = '<\\/span>'

    __url_regex = 'id=[0-9]+\\\\">'
    __url_prefix = 'id='
    __url_sufix = '\\">'

    def __init__(self):
        pass

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        
        print 'INIT: FacebookBot'
        
        self.__br = Browser()
        self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(debug)
        self.__sandman = SandMan('FacebookBot')
        
        self.__lock = Lock()
        try:
            # sign in
            self.__br.open("http://www.facebook.com/login.php")
            self.__br.select_form(nr=0)
            self.__br['email'] = user
            self.__br['pass'] = passw
            resp = self.__br.submit()

            time.sleep(0.2)
            self.__good = True
        except Exception, e:
            print 'EXCEPTION on FacebookBot, possibly bad user/password or https login don\' work behind a proxy.'
            self.__good = False

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
        print '(FacebookBot) searching...'
        url_query = urllib.urlencode({'q':query})
        link = Link()
        link.absolute_url = 'http://www.new.facebook.com/s.php?' + url_query
        resp = self.__br.follow_link(link)
        cont = resp.read()

        sid = re.search('sid=[a-z0-9]+"', cont).group()[4:-1]
        url_query = urllib.urlencode({'q':query, 'sid':sid})
        link.absolute_url = 'http://www.new.facebook.com/s.php?' + url_query
        resp = self.__br.follow_link(link)
        cont = resp.read()
        
        links = re.findall("www.new.facebook.com/friends/\?id=[0-9]+", cont)
        
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
        match = match.group()[len(self.__url_prefix):-len(self.__url_sufix)]
        return 'http://www.facebook.com/friends/?id=' + match

    def friends(self, (names, graph)):
        if not self.__good:
            print 'EXCEPTION on FacebookBot, possibly https login don\' work behind a proxy.'
            return [], {}, {}
        self.__lock.acquire()
        try:
            return self.__impl_friends(names)
        finally:
            self.__lock.release() # release lock, no matter what        

    def __impl_friends(self, names):
        self.__sandman.try_to_sleep()
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
        # retrieve the first n (50?) contacts as tuples (complete_name, facebook_url).
        full_url = name_link # + ('/%s' % type)
        full_url = 'http://%s' % full_url
        resp = self.__br.open( full_url )
        cont =  resp.read()
        matches = re.findall(self.__regex, cont)
        complete_names = map(self.__strip_complete_name, matches)            
        urls = map(self.__strip_url, matches)    
        
        self_attrs, node_dict, link_dict = [], {}, {}
        for name, url in zip(complete_names, urls):
            node_dict[name] = []
            node_dict[name] = [(Attributes.URL_SOURCE_ATTR,url)]
            node_dict[name] += [(Attributes.ALIAS_ATTR,name)]
            node_dict[name] += [(Attributes.FACEBOOK_ALIAS_ATTR,url.split('=')[-1])]                                    
            link_dict[name] = [(Attributes.URL_SOURCE_ATTR,full_url)]
        return self_attrs, node_dict, link_dict
        #return zip(complete_names, urls)

    def is_chatbot(self):
        return False

    def save_cache(self):
        pass



if __name__=='__main__':

    pass

