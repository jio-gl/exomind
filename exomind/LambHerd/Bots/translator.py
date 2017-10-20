import httplib, urllib

class Translate:

	# proxies = ('192.168.254.254',80) for example
	def __init__(self, proxies=None):
		p = {}
		p['callback'] = 'google.language.callbacks.id102'
		p['context']  = 22
		p['key']  = 'notsupplied'
		p['v']  = '1.0'
		self.__params = p
	        if proxies:
	            host = proxies[0]
	            port = proxies[1]
	            self._proxy_conn = httplib.HTTPConnection(host, int(port))
	            self._proxy_conn.connect()
	        else:
	            self._proxy_conn = None

	# src and dst are languages like es, en, de, etc...
	def translate(self, text, src='', dst='en'):
		url_text= urllib
		self.__params['langpair']  = '%s|%s' % (src,dst)
		self.__params['q']  = text
		params = urllib.urlencode(self.__params)
		server = 'www.google.com'
		get = '/uds/Gtranslate?%s' % params
	        if not self._proxy_conn:
        	    self.conn = httplib.HTTPConnection(server)        
                    self.conn.request("GET", get)
        	else:
        	    self.conn = self._proxy_conn
	            self.conn.request("GET", server + get)
		f = self.conn.getresponse()
		prefix = 'google.language.callbacks.id102(\'22\',{"translatedText":"'
		if src=='':
			suffix = '","detectedSourceLanguage":"es"}, 200, null, 200)'
		else:
			suffix = '"}, 200, null, 200)'
		return f.read()[len(prefix):-len(suffix)]

if __name__ == '__main__':
	proxy = {}
	t = Translate(proxy)
	print t.translate('hola mundo!')

