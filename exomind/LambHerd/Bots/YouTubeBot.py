
from exomind.Attributes import Attributes
from exomind.RegexTextTool import RegexTextTool
from SandMan import SandMan

from mechanize import Browser
import time, random

import httplib
import re

class YouTubeBot:
    
    __forb_tags = ['the', 'and', 'their', 'at', 'is', 'in', 'of', 
                   'a', 'on', 'for', 'an', 'with', 'to']    


    __complete_name_prefix = '"http://www.youtube.com/profile\?user='
    __complete_name_sufix = '"'
    __complete_name_central_regex = RegexTextTool.TOKEN_REGEX

    __favorite_prefix = '"http://www.youtube.com/watch\?v='
    __favorite_sufix = '"'
    __favorite_central_regex = RegexTextTool.TOKEN_REGEX
    
    __tag_prefix = ' term=\''
    __tag_sufix = '\'/>'
    __tag_central_regex = RegexTextTool.TOKEN_REGEX

    __forb_tags = ['the', 'and', 'their', 'at', 'is', 'in', 'of', 
                   'a', 'on', 'for', 'an', 'with']    

    def is_chatbot(self):
        return False


    def __init__(self, proxies_per_proto={}, debug=False):
        if proxies_per_proto == {}:
            proxies_per_proto = None        
        self.__proxies = proxies_per_proto
        self.__debug = debug
        self.__handle_robots = False

        self.__sandman = SandMan('YouTubeBot')
        
        #  no sign in
        
        self.__contact_regex_tool = RegexTextTool()
        self.__contact_regex_tool.set_prefix(self.__complete_name_prefix)
        self.__contact_regex_tool.set_suffix(self.__complete_name_sufix)
        self.__contact_regex_tool.set_central_regex(self.__complete_name_central_regex)
        
        self.__favorite_regex_tool = RegexTextTool()
        self.__favorite_regex_tool.set_prefix(self.__favorite_prefix)
        self.__favorite_regex_tool.set_suffix(self.__favorite_sufix)
        self.__favorite_regex_tool.set_central_regex(self.__favorite_central_regex)
        
        self.__tag_regex_tool = RegexTextTool()
        self.__tag_regex_tool.set_prefix(self.__tag_prefix)
        self.__tag_regex_tool.set_suffix(self.__tag_sufix)
        self.__tag_regex_tool.set_central_regex(self.__tag_central_regex)

    def read_url(self, url, get):        
        if not self._proxy_conn:
            self.conn = httplib.HTTPConnection(url)        
            self.conn.request("GET", get)
        else:
            self.conn = self._proxy_conn
            self.conn.request("GET", 'http://' + url + get)

        if self.__debug:
            print 'http://' + url + get 

        r1 = self.conn.getresponse()        
        p = r1.read()
        return p
        
    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        self.set_proxies_per_proto(proxies_per_proto)
        
    def set_sleep_secs(self, secs):
        self.__sandman.set_sleep_secs(secs)        

    def set_sleep_module(self, iterations):
        self.__sandman.set_sleep_module(iterations)        

    def set_sleep_failure(self, secs):
        self.__sandman.set_sleep_failure(secs)

    def set_sleep_random_flag(self, bool):
        self.__sandman.set_sleep_random_flag(bool)

    def set_proxies_per_proto(self, proxies):
        self.__proxies = proxies
        if proxies and 'http' in proxies:
            host = proxies['http'].split(':')[0]
            port = proxies['http'].split(':')[1]
            try:
                self._proxy_conn = httplib.HTTPConnection(host, int(port))
                self._proxy_conn.connect()
            except:
                print 'EXCEPTION on YouTubeBot, possibly bad user/password or https login don\' work behind a proxy.'

        else:
            self._proxy_conn = None

    #most_viewed
    #top_rated
    #recently_featured
    #watch_on_mobile
    def seeds(self, type='most_viewed'):
        self.__sandman.try_to_sleep()
        cont = self.read_url('gdata.youtube.com', '/feeds/standardfeeds/' + type)
        self.__contact_regex_tool.set_text(cont)
        return self.__contact_regex_tool.extract_elements()        

    def search(self, query):

        # check if name exists.
        try:
            print '(YouTubeBot) searching...'
            self.__sandman.try_to_sleep()
            cont = self.read_url('gdata.youtube.com', '/feeds/users/%s/favorites' % query)
        except Exception, e:
            if str(e) == 'HTTP Error 404: Not Found':
                return []
            else:
                raise e
        return [cont]

    def users_from_favorite_videos(self, (names, graph)):
        return self.contacts(names)

    def __normalize_tags(self, tags):
        tags = map(lambda x: x.lower(), tags)        
        tags = filter(lambda x: x not in self.__forb_tags, tags)        
        return tags

    def contacts(self, names):
        """
        search for display name "name" and retrieves contact as tuples (display_name, url).
        precondition: self.exists(user)
        """
        # check if name exists.
        for name in names:
            results = self.search(name)
            if len(results) != 0:
                break

        if len(results) == 0:
            return {}, {}
    
        cont = results[0]
        # favorite authors as contacts.
        self.__contact_regex_tool.set_text(cont)        
        complete_names = self.__contact_regex_tool.extract_elements()
        # favorite videos to extract tags of relation.
        self.__favorite_regex_tool.set_text(cont)
        favorite_videos = self.__favorite_regex_tool.extract_elements()

        # remove repetitions
        aux = []
        for fav in favorite_videos:
            if not fav in aux:
                aux.append(fav)
        favorite_videos = aux
        # retrieve tags for each video
        tags_videos = []
        for fav in favorite_videos:
            self.__sandman.try_to_sleep()	    
            cont = self.read_url('gdata.youtube.com', '/feeds/videos/%s' % fav)
            self.__tag_regex_tool.set_text(cont)
            tags = self.__tag_regex_tool.extract_elements()
            tags = self.__normalize_tags(tags)
            tags_videos.append(tags)

        self_attrs, node_dict, link_dict = [], {}, {}
        for neigh, tags in zip(complete_names, tags_videos):
            if neigh != name: 
                if not neigh in link_dict:
                    link_dict[neigh] = []
                if not neigh in node_dict:
                    node_dict[neigh] = []                
                for tag in tags:
                    link_dict[neigh] += [(Attributes.TAG_ATTR,tag)]
                link_dict[neigh] += [(Attributes.YOUTUBE_ALIAS_ATTR,'')]
                node_dict[neigh] += [(Attributes.YOUTUBE_ALIAS_ATTR,neigh)]
                node_dict[neigh] += [(Attributes.ALIAS_ATTR,neigh)]

        for neigh in link_dict:
            link_dict[neigh] = list(set(link_dict[neigh]))
            node_dict[neigh] = list(set(node_dict[neigh]))
        return self_attrs, node_dict, link_dict        
    
    def __lifo_pop(self, stack):
        return stack.pop()

    def __fifo_pop(self, stack):
        return stack.pop(0)

    def __lifo_retrieve(self, stack, item):
        stack.append(item)

    def __fifo_retrieve(self, stack, item):
        stack = [item] + stack

    def expander(self, name):
        if name == 'users_generating_favorite_videos':
            return self.contacts
        else:
            raise Exception('expander method %s unknown in YouTubeBot')

    def save_cache(self):
        pass

if __name__ == '__main__':
        bot = YouTubeBot()
        bot.initialize({})
        seeds = bot.seeds()        
        print str(seeds)

