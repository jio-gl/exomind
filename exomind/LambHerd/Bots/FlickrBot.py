
from exomind.Attributes import Attributes
from exomind.RegexTextTool import RegexTextTool
from SandMan import SandMan

from mechanize import Browser
import time, random

import urllib, urllib2, httplib
import re

class FlickrBot:

    # use favorite authors as contacts.
    __url = 'http://www.flickr.com'

    __favorites_url = 'http://www.flickr.com/photos/%s/favorites'

    __favorite_regex = '/photos/[a-zA-Z_0-9@]+/[0-9]+/'
    __favorite_prefix = ''
    __favorite_sufix = ''    

    __contact_regex = __favorite_regex

    __complete_name_regex = __contact_regex
    __complete_name_prefix ='/photos/' 
    __complete_name_sufix = '/'

    __tag_regex = '/photos/tags/[a-zA-Z_0-9\-]+/'

    __tag_prefix = '/photos/tags/'
    __tag_sufix = '/'

    __forb_tags = ['the', 'and', 'their', 'at', 'is', 'in', 'of', 'a', 'on', 'for', 'an', 'with']    

    def __init__(self, proxies_per_proto={}, debug=False):
        self.__br = Browser()
        self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(debug)
        # no respect for robots.txt
        self.__br.set_handle_robots(False)
        
        self.__sandman = SandMan('FlickrBot')
        #  no sign in
        self.__debug = False

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        pass

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
                print 'EXCEPTION on FlickrBot, possibly bad user/password or https login don\' work behind a proxy.'

        else:
            self._proxy_conn = None

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

    #most_viewed
    #top_rated
    #recently_featured
    #watch_on_mobile
    def seeds(self):
        self.__sandman.try_to_sleep()
#        resp = urllib.urlopen('http://www.flickr.com/', self.__proxies)
#        cont = resp.read()
	cont = self.read_url('www.flickr.com', '/')
        matches = re.findall(self.__contact_regex, cont)
        users  = map(self.__strip_complete_name, matches)
        return users

    def search(self, query):

        br = self.__br
        # check if name exists.
        try:
            url = 'http://www.flickr.com/photos/%s/favorites/' % query
            #print url
            self.__sandman.try_to_sleep()
            #resp = urllib.urlopen(url, self.__proxies)
            #cont =  resp.read()
            cont = self.read_url('www.flickr.com', '/photos/%s/favorites/' % query)
            if not 'favorites' in cont:
                return []
        except Exception, e:
            if str(e) == 'HTTP Error 404: Not Found':
                return []
            else:
                raise e
        return [cont]

    def __strip_complete_name(self, html_match):
        return html_match.split('/')[2]

    def __strip_url(self, html_match):
        match = re.search(self.__favorite_regex, html_match)
        match = match.group()[len(self.__favorite_prefix):]
        return match

    def __strip_tag(self, html_match):
        match = re.search(self.__tag_regex, html_match)
        match = match.group()[len(self.__tag_prefix):-len(self.__tag_sufix)]
        return match

    def users_from_favorite_photos(self, (names, graph)):
        return self.contacts(names)

    # search for display name "name" and retrieves contact as tuples (display_name, url).
    # precondition: self.exists(user)
    def contacts(self, names):
        br = self.__br
        # check if name exists.
        for name in names:        
            results = self.search(name)
            if len(results) != 0:
                break
                #raise Exception('user "%s" doesn\'t exist in Flickr' % name)
        if len(results) == 0:
            return {}, {}

        cont = results[0]
        
        # favorite videos to extract tags of relation.
        matches = re.findall(self.__favorite_regex, cont)
                # remove repetitions
        favorite_videos  = list(set(matches))
        # favorite authors as contacts.
        complete_names = map(lambda x: x.split('/')[2], favorite_videos)

        # retrieve tags for each photo
        tags_videos = []
        for fav in favorite_videos:
            self.__sandman.try_to_sleep()
            url = self.__url + fav
            #print url
#            resp = urllib.urlopen(url, self.__proxies)
#            cont =  resp.read()
            s_url = url.split('/')
            cont = self.read_url(s_url[2], '/' + '/'.join(s_url[3:]))
            matches = re.findall(self.__tag_regex, cont)
            tags  = map(self.__strip_tag, matches)
            # uniques
            tags = list(set(tags))
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
                node_dict[neigh] += [(Attributes.FLICKR_ALIAS_ATTR,neigh)]
                node_dict[neigh] += [(Attributes.ALIAS_ATTR,neigh)]

        for neigh in link_dict:
            link_dict[neigh] = list(set(link_dict[neigh]))
            node_dict[neigh] = list(set(node_dict[neigh]))
        return self_attrs, node_dict, link_dict        

    def is_chatbot(self):
        return False


    def __normalize_tags(self, tags):
        #forb_regexs = ['\$[^\n\$]+\$']
        tags = map(lambda x: x.lower(), tags)
        tags = filter(lambda x: x not in self.__forb_tags, tags)
        return tags

    def save_cache(self):
        pass


