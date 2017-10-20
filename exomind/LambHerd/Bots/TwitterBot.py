
from exomind.Attributes import *
from exomind.ExomindException import BotException
from SandMan import SandMan
from distance import NGD

from mechanize import Browser
import urllib2, urllib
import re, time
import sys, traceback


from threading import Lock

class TwitterBot:

    __favorites_regex = '<a href="http://twitter.com/[a-zA-Z0-9_]+" title="[a-zA-Z0-9\-_ .]+">[a-zA-Z0-9_]+</a>'
    
    __following_regex = '<a href="http://twitter.com/[a-zA-Z0-9_]+" rel="contact"><img alt="[a-zA-Z0-9\-_ .]+" class'
    
    __fav_complete_name_regex = 'title="[a-zA-Z0-9\-_ .]+">'    
    __fav_complete_name_prefix = 'title="'
    __fav_complete_name_sufix = '">'

    __foll_complete_name_regex = 'img alt="[a-zA-Z0-9\-_ .]+" class'    
    __foll_complete_name_prefix = 'img alt="'
    __foll_complete_name_sufix = '" class'
    
    __url_regex = 'href="http://twitter.com/[a-zA-Z0-9_]+" '
    __url_prefix = 'href="'
    __url_sufix = '" '

    def __init__(self):
        pass

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):

        print 'INIT: TwitterBot'
        
        self.__br = Browser()
        self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(debug)
        self.__debug = debug
        self.__sandman = SandMan('TwitterBot')
        
        self.__ngd = NGD()
        self.__ngd.set_proxies(proxies_per_proto)
        
        self.__lock = Lock()
        try:
            # sign in
            self.__br.open("http://twitter.com/")
            self.__br.select_form(nr=1)
            self.__br['session[username_or_email]'] = user
            self.__br['session[password]'] = passw
            resp = self.__br.submit()
            time.sleep(0.2)
    
        except Exception, e:
            if self.__debug:
                traceback.print_exc(file=sys.stdout)
                print str(e)            
            print 'EXCEPTION on TwitterBot, possibly bad user/password or https login don\' work behind a proxy.'

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
        print '(TwitterBot) searching...'

#        br = self.__br
#        params = urllib.urlencode({'q': query})
#        f = urllib.urlopen("http://twitter.com/tw/search/users?%s" % params)
#        cont = f.read()
#        
#        links = re.findall("twitter.com/[a-zA-Z_]+", cont)
#        # remove repetitions
#        links = list(set(links))
#        
#        links_urls = []
#        for link in links:
#            if  not 'index.php' in link and \
#                not 'twitter.com/blog' in link and \
#                not 'twitter.com/invitations' in link and \
#                not 'twitter.com/images' in link and \
#                not 'twitter.com/stylesheets' in link and \
#                not 'twitter.com/javascripts' in link and \
#                not 'twitter.com/home' in link:
#                links_urls.append(link)
#                #print 'search url: %s' % link.url
        
        #br.back()
        #return ['twitter.com/earlkman']
        
        links_urls = self.__ngd.links_query(query + ' site:twitter.com', 1)
        links_urls = map(lambda x: '/'.join(x.split('/')[2:4]), links_urls)
        
        return links_urls

    def __strip_foll_complete_name(self, html_match):
        match = re.search(self.__foll_complete_name_regex, html_match)
        match = match.group()[len(self.__foll_complete_name_prefix):-len(self.__foll_complete_name_sufix)]
        return match

    def __strip_fav_complete_name(self, html_match):
        match = re.search(self.__fav_complete_name_regex, html_match)
        match = match.group()[len(self.__fav_complete_name_prefix):-len(self.__fav_complete_name_sufix)]
        return match

    def __strip_url(self, html_match):
        match = re.search(self.__url_regex, html_match)
        match = match.group()[len(self.__url_prefix):-len(self.__url_sufix)]
        return match

    def following(self, (names, graph)):
        self.__lock.acquire()
        try:
            return self.__contacts(names, 'friends')
        finally:
            self.__lock.release() # release lock, no matter what        

    def followers(self, (names, graph)):
        self.__lock.acquire()
        try:
            return self.__contacts(names, 'followers')
        finally:
            self.__lock.release() # release lock, no matter what        

    def favorites(self, (names, graph)):
        self.__lock.acquire()
        try:
            return self.__contacts(names, 'favourites')
        finally:
            self.__lock.release() # release lock, no matter what        

    def __contacts(self, names, type='following'):
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
        # retrieve the first n (20?) contacts as tuples (complete_name, twitter_url).
        full_url = name_link # + ('/%s' % type)
        resp  = self.__br.open('http://%s/%s' % ( full_url, type ) )
            
        cont =  resp.read()
        if type == 'friends' or type == 'followers':  
            matches = re.findall(self.__following_regex, cont)
            complete_names = map(self.__strip_foll_complete_name, matches)            
        else:
            matches = re.findall(self.__favorites_regex, cont)
            complete_names = map(self.__strip_fav_complete_name, matches)            
        urls = map(self.__strip_url, matches)    
        
        self_attrs, node_dict, link_dict = [], {}, {}
        for name, url in zip(complete_names, urls):
            if type == 'followers':
                dict_name = '__INVERSE__' + name
            else:
                dict_name = name
                
            node_dict[dict_name] = []
            #node_dict[name] = [(Attributes.URL_SOURCE_ATTR,url)]
            node_dict[dict_name] += [(Attributes.ALIAS_ATTR,name)]
            node_dict[dict_name] += [(Attributes.TWITTER_ALIAS_ATTR,url.split('/')[-1])]
            node_dict[dict_name] += [(Attributes.ALIAS_ATTR,url.split('/')[-1])]                        
            #link_dict[name] = [(Attributes.URL_SOURCE_ATTR,full_url)]
        return self_attrs, node_dict, link_dict

    def is_chatbot(self):
        return False

    def save_cache(self):
        pass



if __name__=='__main__':

    pass


