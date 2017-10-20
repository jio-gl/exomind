

import unittest

from pprint import pprint

from RegexTextTool import RegexTextTool

class RegexTextToolTest(unittest.TestCase):
    
    """
    A test class for class RegexTextTool.
    """
    
    __html_text= """
<head>
    <title>Flickr: Fotos de tito</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="keywords" content="fotografa, fotografa digital, telfonos con cmara, cmara, fotografa como pasatiempo, foto, cmara digital, compactflash, smartmedia, cmaras, canon, nikon, olympus, fujifilm">    
    <meta name="description" content="Flickr es casi con seguridad la mejor aplicacin de todo el mundo para administrar y compartir fotos en lnea. Presume de tus fotos favoritas ante el mundo, mustrales fotos a tus familiares y amigos con seguridad y privacidad, o publica en un blog las fotos que tomas con un telfono con cmara.">
    <meta http-equiv="imagetoolbar" content="no">
    <meta name="viewport" content="width=820" />
    <link href="http://l.yimg.com/www.flickr.com/css/c_flickr.css.v1.806.14" rel="stylesheet" type="text/css">

      <link rel="alternate"    type="application/atom+xml" title="Flickr: Fotos de tito Atom feed" href="http://api.flickr.com/services/feeds/photos_public.gne?id=79298923@N00&amp;lang=es-us&amp;format=atom">
    <link rel="alternate"    type="application/rss+xml" title="Flickr: Fotos de tito RSS feed" href="http://api.flickr.com/services/feeds/photos_public.gne?id=79298923@N00&amp;lang=es-us&amp;format=rss_200">

    <link rel="shortcut icon" type="image/ico" href="/favicon.ico">

<link href="http://l.yimg.com/www.flickr.com/css/c_person.css.v1.39.14" rel="stylesheet" type="text/css" />
    
    """
    
    def setUp(self):
        """
        set up data used in the tests.
        setUp is called before each test function execution.
        """
        self.__tool = RegexTextTool(self.__html_text)

    def testExtractElements(self):
        """
        Test a successful run of the RegexTextTool seeds
        """
        print "RegexTextToolTest.testExtractElements()"
        
        self.__tool.set_prefix('http://')
        self.__tool.set_suffix('/')
        self.__tool.set_central_regex('[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+')
        elems = self.__tool.extract_elements()
        pprint(elems)

        self.assertEqual(4, len(elems))
        
        
    def tearDown(self):
        """
        tear down any data used in tests
        tearDown is called after each test function execution.
        """
        pass

if __name__ == '__main__':
    unittest.main()     