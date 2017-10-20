
import httplib, urllib
import re
import math
import time
import pickle

# thread imports
from nsedthread import NSEDThread

class Cache:
    def __init__(self, max_size=1000):
        self.__max = max_size
        self.__dict = {}
    def __getitem__(self, key):
        try:
            item = self.__dict[key]
        except:
            item = None
        return item
    def __setitem__(self, key, item):
        if not key in self.__dict and len(self.__dict) >= self.__max:
            # remove one
            del self.__dict[ list(self.__dict.keys())[0] ]
        self.__dict[key] = item
    def has_key(self, key):
        return self.__dict.has_key(key)
    def __str__(self):
        return str(self.__dict)
    def keys(self):
        return self.__dict.keys()

class QueryResult:
    def __init__(self, link, cache_link, snippet,title):
        self.title      = title
        self.link       = link
        self.cache_link = cache_link
        self.snippet    = snippet

    def __str__(self):
        return str((self.title, self.link, self.cache_link, self.snippet))

# Normalized Search Engine Distance
class NSED(object):

    def __search_engine_strip(self):
        return ''

    def __load_cache(self):
        # experimental persistent cache.
        try:
            pkl_file = open('NSED.cache', 'rb')
            cache = pickle.load(pkl_file)
            pkl_file.close()
        except:
            cache = Cache()
        return cache
        
    def save_cache(self):
        output = open('NSED.cache', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.__cache, output)
        output.close()
        
    def __init__(self, url, get, regex, strip, params, qparam, proxies=None):
        self.__base = 2
        self.__url = url
        self.__get = get
        self.__regex = regex
        self.__strip = strip
        self.__params = params
        self.__qparam = qparam
        self.__cache = self.__load_cache()
        self.__failures = 0
        self.set_proxies(proxies)
        self.set_context('')
        self._params = params
        self.__debug = False
        

    def set_proxies(self, proxies=None):
        self.__proxies = proxies
        if proxies and 'http' in proxies:
            host = proxies['http'].split(':')[0]
            port = proxies['http'].split(':')[1]
            try:
                self._proxy_conn = httplib.HTTPConnection(host, int(port))
                self._proxy_conn.connect()
            except:
                self._proxy_conn = None
        else:
            self._proxy_conn = None

    def set_sleep_secs(self, secs):
        self.__sleep_secs = float(secs)

    def set_sleep_module(self, iterations):
        self.__sleep_module = iterations

    def set_sleep_failure(self, secs):
        self.__sleep_failure = float(secs)        

    def set_sleep_random_flag(self, bool):
        self.__sleep_random_flag = bool        

    def update_params(self, key, val):
        self.__params[key] = val

    def clear_failures(self):
        self.__failures = 0

    def get_failures(self):
        return self.__failures

    def set_context(self, context):
        self.__context = context
        # results for letter 'a' as approximation of total pages indexed
        self.__total = self.results('a', context)

    def get_context(self):
        return self.__context

    def get_base(self):
        return self.__base

    def results_total(self):
        return self.__total

    def __add_quotes(self, str):
        if str.find(' ') != -1 and len(str)>0 and str[0]!='"' and str[-1]!='"':
            return '"' + str + '"'
        else:
            return str

    # quotes are not implicit in context, but are in string
    def results(self, string, context=None):
        if context and context!=self.__context:
            self.set_context(context)
        else:
            context = self.__context        
        if context!=self.__context:
            self.set_context(context)
        res = self.results_list([string, context])
        return res 

    # avoid unescaped double quotes in string
    def results_query(self, string):
        # first check cache
        ms = self.matches_query(string)
        if len(ms) == 0:
            res = 0
            self.__failures += 1
        else:            
            res = long(ms[0])
        return res

    def __strip_link(self, link):
        link = link.group()
        return link[9:-9]

    def __strip_link_cache(self, link):
        link = link.group()
        return link[9:]

    def __strip_snippet(self, snippet):
        snippet = snippet.group()
        return snippet[15:-4]

    def __strip_title(self, title):
        title = title.group()
        return title[8:-4]

    def links_query(self, string, num=100):
        self.__params['num'] = num
        ret = self.matches_query(string, '<a href="http://[\+a-zA-Z./0-9\?\_=&,;%]+" class=l', self.__strip_link)
        self.__params['num'] = 1
        return ret

    def links_cache_query(self, string, num=100):
        self.__params['num'] = num
        ret = self.matches_query(string, '<a href="http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/search\?q=cache:[\+a-zA-Z./0-9\?\_=&,;%:]+', self.__strip_link_cache)
        self.__params['num'] = 1
        return ret

    def snippets_query(self, string, num=100):
        self.__params['num'] = num
        ret = self.matches_query(string, '<div class="s">([^<]*(<b>)*(</b>)*(<em>)*(</em>)*)*<br>', self.__strip_snippet)
        self.__params['num'] = 1
        return ret

    def titles_query(self, string, num=100):
        self.__params['num'] = num
        ret = self.matches_query(string, 'class=l>([^<]*(<b>)*(</b>)*(<em>)*(</em>)*)*</a>', self.__strip_title)
        self.__params['num'] = 1
        return ret

    def query(self, string):
        ret = []
        links = self.links_query(string)
        cache_links = self.links_cache_query(string)
        snippets = self.snippets_query(string)
        titles = self.titles_query(string)
        for i in range(len(links)):
            ret.append(QueryResult(links[i],cache_links[i],snippets[i],titles[i]))
        return ret

    def do_req(self, string):        
        url_string = string + ' ' + self.__add_quotes(self.__context)
        self.__params[self.__qparam] = url_string
        url_params = urllib.urlencode(self.__params)
        if not self._proxy_conn:
            self.conn = httplib.HTTPConnection(self.__url)        
            self.conn.request("GET", self.__get + url_params)
        else:
            self.conn = self._proxy_conn
            self.conn.request("GET", 'http://' + self.__url + self.__get + url_params)

#        if self.__debug:
#        print 'http://' + self.__url + self.__get + url_params 

        r1 = self.conn.getresponse()        
        p = r1.read()
#        print p
        return p

    # avoid unescaped double quotes in string
    def matches_query(self, string, regex=None, strip=None):
        if self.__cache.has_key(str((string,self.__params['num']))):
            p = self.__cache[str((string,self.__params['num']))]
        else:
            p = self.do_req(string)
            self.__cache[str((string,self.__params['num']))] = p
        if not regex:
            regex = self.__regex
            strip = self.__strip
        iterator = re.finditer(regex, p)
        ret = []
        for match in iterator:
            ret.append(strip(match))
        return ret

    def results_list(self, list):
        string = ''
        for s in list:
            string += self.__add_quotes(s) + ' '
        return self.results_query(string)
    
    def only_entropy(self, string, context=None):
        res, ent, norm_ent = self.entropy(string, context)
        return norm_ent
    
    def only_results(self, string, context=None):
        res, ent, norm_ent = self.entropy(string, context)
        return res
    
    # return num_hits, entropy, normalized_entropy
    def entropy(self, string, context=None):
        if context and context!=self.__context:
            self.set_context(context)
        else:
            context = self.__context
        results = self.results(string, context)
        if results != 0:
            ent = - math.log(float(results)/self.__total, self.__base)
            max_ent = self.__max_entropy(context)
            norm_ent = (max_ent - ent) / max_ent
            ent = max_ent - ent 
        else:
            ent, norm_ent = 0.0, 0.0
        return results, ent, norm_ent

    def __max_entropy(self, context=None):
        if context and context!=self.__context:
            self.set_context(context)
        else:
            context = self.__context        
        return - math.log(1.0/self.__total, self.__base)

    def max_entropy(self):
        return 1, self.__max_entropy(), 1.0

    def min_entropy(self):
        return self.results_total(), 0.0, 0.0

    # quotes are not implicit in context, but are in x and y.
    def distance(self, (x, y), context=None):
        return self.__distance((x, y), context, self.__norm_se_dist)

    def jaccard_distance(self, (x, y), context=None):
        return self.__distance((x, y), context, self.__jaccard_dist)

    def hits_distance(self, (x, y), context=None):
        return self.__distance((x, y), context, self.__hits_dist)

    def __distance(self, (x, y), context=None, func=None):
        if context and context!=self.__context:
            self.set_context(context)
        else:
            context = self.__context
        x_res = self.results(x, context)
        y_res = self.results(y, context)
        # x,y results as a set, not concatenation
        xy_res = self.results_list([x,y,context])
        # use base 2 logs to compute final value
        return func(x_res, y_res, xy_res, self.__total, self.__base)
    
    def __norm_se_dist(self, x_res, y_res, xy_res, total, base):
        if x_res==0 or y_res==0 or xy_res==0:
            return None
        base = self.__base
        numerator = max( math.log(x_res,base), math.log(y_res,base) ) - math.log(xy_res,base)
        denominator = math.log(total,base) - min( math.log(x_res,base), math.log(y_res,base) )
        ret = numerator / denominator
        return ret 

    def __jaccard_dist(self, x_res, y_res, xy_res, total, base):
        if x_res==0 and y_res==0:
            return None
        if xy_res==0:
            return None # assume equal
        base = self.__base
        numerator = xy_res
        denominator = x_res + y_res - xy_res
        if denominator > 0:
            ret = float(numerator) / denominator
        else:
            ret = 0.0
        return ret 

    def __hits_dist(self, x_res, y_res, xy_res, total, base):
        return xy_res

    def distances(self, pairs, context=None, use_threads=True):
        if context and context!=self.__context:
            self.set_context(context)
        else:
            context = self.__context
        if use_threads:
            return self.__fast_distances(pairs, context)
        else:
            dists = {}
            for p in pairs:
                dists[p] = self.distance(p,context)
            return dists

    def __fast_distances(self, pairs, context=''):
        dists = {}
        threads = 8
        size = 8
    
        partial = 0
        while partial < len(pairs):
    
            threadlist = []
            thread_count = 0
            while thread_count < threads and partial < len(pairs):
                thread_instance = NSED(self.__url, self.__get, self.__regex, self.__strip, self.__params, self.__qparam, self.__cache)
                current = NSEDThread(thread_instance, pairs[partial:partial+size], context)
                partial += size
                threadlist.append(current)
                current.start()
                thread_count += 1
    
            for thread in threadlist:
                thread.join()
                dists.update(thread.distances)
    
        return dists
               
   
        
