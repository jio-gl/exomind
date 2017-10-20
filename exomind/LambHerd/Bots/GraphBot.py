
from exomind.Attributes import *
from exomind.ExomindException import BotException
from SandMan import SandMan
from exomind.pyRijndael import EncryptData, DecryptData

from mechanize import Browser
import urllib2, urllib
import re, time, base64


from threading import Lock

class GraphBot:

    passw = None

    def is_chatbot(self):
        return False

    def __init__(self):
        pass

    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):
        print 'INIT: GraphBot'
        self.__pass = passw
        # hack to acces password
        self.__class__.passw = passw
        
    def set_proxies_per_proto(self, proxies):
        pass

    def set_sleep_secs(self, secs):
        pass

    def set_sleep_module(self, iterations):
        pass

    def set_sleep_failure(self, secs):
        pass

    def set_sleep_random_flag(self, bool):
        pass

    def neighbors(self, (names, graph)):
        self_attrs, node_dict, link_dict = [], {}, {}
        node = None
        for name in names:
            if graph.has_node(name):
                node = name
                break
        if not node:
            return self_attrs, node_dict, link_dict
        
        for same_node, node2 in graph.edges():            
            node_dict[node2] = []
            node_dict[node2] += [(Attributes.ALIAS_ATTR,node2)]
        return self_attrs, node_dict, link_dict

    def with_all(self, (names, graph)):
        self_attrs, node_dict, link_dict = [], {}, {}
        node = None
        for name in names:
            if graph.has_node(name):
                node = name
                break
        if not node:
            return self_attrs, node_dict, link_dict
        
        for node2 in graph.nodes():
            if node2 != node:            
                node_dict[node2] = []
                node_dict[node2] += [(Attributes.ALIAS_ATTR,node2)]
        return self_attrs, node_dict, link_dict
    
    @classmethod
    def encrypt(cls, string, key=None):
        if not key:
            key = cls.passw
        encry = EncryptData(key, string)
        encod = base64.b64encode(encry)
        return encod
    
    @classmethod
    def decrypt(cls, string, key=None):
        if not key:
            key = cls.passw
        decod = base64.b64decode(string)
        decry = DecryptData(key, decod)
        return decry
    
    def __ofuscate_attr(self, (type, attr)):        
        return (type, GraphBot.encrypt(attr))
    
    def ofuscate(self, val, params, node=None):
        final_self_attrs, final_node_dict, final_link_dict = val
        final_self_attrs = map(self.__ofuscate_attr, final_self_attrs)
        for node in final_node_dict:
            final_node_dict[node] = map(self.__ofuscate_attr, final_node_dict[node])
        for node in final_link_dict:
            final_link_dict[node] = map(self.__ofuscate_attr, final_link_dict[node])
        return final_self_attrs, final_node_dict, final_link_dict

    def save_cache(self):
        pass