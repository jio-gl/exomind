from nsed import NSED

# Normalized Google Search Distance
class NGD(NSED):

    def __google_strip(self, match):
        s = match.group().replace('about ','')
        return s[len('swrnum='):-len('"')].replace(',','')

    def __init__(self, proxies=None):
        url = 'www.google.com'
        get = '/search?'
        params = {}
        params['num'] = '1'
        params['btnG'] = 'Search'
        params['hl'] = 'en'        
        qparam = 'q'
        #regex = '</b> of about [0-9,]+</b> for <b>'
        regex = 'swrnum=[0-9]+"'
        strip = self.__google_strip
        super(NGD,self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0
        self.__debug = False

# Normalized Google Groups Distance
class NGGD(NSED):

    def __google_groups_strip(self, match):
        s = match.group()
        return s[len('of about <b>'):-len('</b>')].replace(',','')

    def __init__(self, proxies=None):
        url = 'groups.google.com'
        get = '/groups/search?'
        params = {}
        params['num'] = '1'
        params['qt_s'] = 'Search+Groups'                
        qparam = 'q'
        regex = 'of about <b>[0-9,]+</b>'
        strip = self.__google_groups_strip
        super(NGGD,self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0
        self.__debug = False

# Normalized Msn Search (now Live Search) Distance
class NMD(NSED):

    def __msn_strip(self, match):
        return match.group()[len('Page 1 of '):-len(' results</span>')].replace(',','')

    def __init__(self, proxies=None):
        url = 'search.live.com'
        get = '/results.aspx?'
        params = {}
        params['go'] = ''
        params['form'] = 'QBRE'        
        qparam = 'q'
        regex = 'Page 1 of .* results</span>'
        strip = self.__msn_strip
        super(NMD,self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0

# Normalized Yahoo Search Distance
class NYD(NSED):

    def __yahoo_strip(self, match):
                return match.group()[len('1 - 10 of '):-len(' for ')].replace(',','')

    def __init__(self, proxies=None):
        url = 'search.yahoo.com'
        get = '/search?'
        params = {}
        qparam = 'p'
#        <span id="infototal">16900000000</span>
        regex = '1 - 10 of [0-9,]+ for '
        strip = self.__yahoo_strip
        super(NYD,self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0

# Fotolog Harvester
class Fotolog(NSED):

    def __fotolog_strip(self, match):
        return match.group()[len('www.fotolog.com/'):-len('/')].replace(',','')

    def __init__(self):
        url = 'ff.fotolog.com'
        get = '/all.html?p=%s'
        params = {}
        qparam = 'u'
        regex = 'www.fotolog.com\/[a-z0-9_-]+\/'
        strip = self.__yahoo_strip
        super(NYD,self).__init__(url, get, regex, strip)
        self.__failures = 0

if __name__ == '__main__':
#    proxies = {'http':'192.168.254.254:80'}
#    
#    d = NGD(proxies)
#    #d = NYD(proxies)
#    print d.distance(('Fernando Miranda', 'fmiranda'))
    
    from distance import NGGD
    d = NGGD()
    print d.distance(('obama','mccain'))
    print d.snippets_query('obama')
    
#    l = d.links_query('site:facebook.com "Diego Tiscornia"')
##    #print l
#    print len(l)    
#    ls = d.links_cache_query('site:facebook.com "Diego Tiscornia"')
#    #print ls
#    print len(ls)
#    s =  d.snippets_query('site:facebook.com "Diego Tiscornia"')
#    #print s
#    print len(s)
#    s =  d.titles_query('site:facebook.com "Diego Tiscornia"')
#    #print s
#    print len(s)
#    #print d.distance(('Hernan Ochoa', 'hochoa'))
#    #print d.distance(('Hernan Ochoa', 'hochoa'))