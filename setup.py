#!/usr/bin/env python

from distutils.core import setup
import os.path

setup(name='Exomind',
      version='0.1',
      description='Open Source Intelligence Library',
      author='Jose Orlicki',
      author_email='name.surname@coresecurity.com',
      url='http://corelabs.coresecurity.com',
      packages=['exomind', 'exomind.LambHerd', 'exomind.LambHerd.Bots', 'exomind.algorithm'],
      package_data={'exomind': ['data/*', 'examples/*', 'doc/*']},
      requires=['MySQLdb', 'mechanize', 'pygraphviz (==0.37)'],
      data_files=[(os.path.expanduser('~') + '/.exomind', ['.exomind/exomind.xml',
				  '.exomind/expanders.xml',
				  '.exomind/weigh_scales.xml',
				  '.exomind/bots.xml',
				  '.exomind/expanders.xml.proxy',
				  '.exomind/bots.xml.proxy',
				  '.exomind/expanders.xml.no_proxy',
				  '.exomind/bots.xml.no_proxy',
				  '.exomind/syn_map.pickle',]),
		  (os.path.expanduser('~') + '/.exomind/msnbot',['.exomind/msnbot/bla@hotmail.com'])
		 ]     
)


