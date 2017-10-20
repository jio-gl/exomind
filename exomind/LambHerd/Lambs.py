
from Bots import *
from exomind.ExomindException import *
from exomind.Utils import getText

import xml.dom.minidom
import os.path


class BotException(Exception):
    pass

class Lambs:
    
    def __init__(self, sleep_failure=0.0, proxies_per_proto = {}):
        
        self.__sleep_failure = sleep_failure
        self.__proxies_per_proto = proxies_per_proto
        
        self.__lambs = {}
        
        self.__load_bots()
        self.__load_expanders()
        self.__load_weigh_scales()
        
    def __load_bots(self):
        
        path =  '/.exomind/bots.xml'
        try:
            full_path = os.path.expanduser('~') + path
            f = open(full_path)
        except Exception, e:
            try:
                full_path = '.' + path
                f = open(full_path)
            except Exception, e:                
                raise e
        dom = xml.dom.minidom.parseString(f.read())
        f.close()
        
        bots = dom.getElementsByTagName('bot')
        for bot in bots:
            self.__load_bot(bot)
            
    def __load_expanders(self):

        path =  '/.exomind/expanders.xml'
        try:
            full_path = os.path.expanduser('~') + path
            f = open(full_path)
        except Exception, e:
            try:
                full_path = '.' + path
                f = open(full_path)
            except Exception, e:                
                raise e
        dom = xml.dom.minidom.parseString(f.read())
        f.close()
        
        expanders = dom.getElementsByTagName('expander')
        self.__expanders = {}
        for expander in expanders:
            self.__load_expander(expander)

    def __load_weigh_scales(self):

        path =  '/.exomind/weigh_scales.xml'
        try:
            full_path = os.path.expanduser('~') + path
            f = open(full_path)
        except Exception, e:
            try:
                full_path = '.' + path
                f = open(full_path)
            except Exception, e:                
                raise e
        dom = xml.dom.minidom.parseString(f.read())
        f.close()
        
        weigh_scales = dom.getElementsByTagName('weigh_scale')
        self.__weigh_scales = {}
        self.__weigh_scales_params = {}
        for weigh_scale in weigh_scales:
            self.__load_weigh_scale(weigh_scale)

    def __load_bot(self, dom):
        
        attrs = {}
        
        attrs['class'] = getText(dom.getElementsByTagName('class')[0].childNodes)
        attrs['user'] = getText(dom.getElementsByTagName('user')[0].childNodes)
        attrs['pass'] = getText(dom.getElementsByTagName('pass')[0].childNodes)
        attrs['sleep_regular_secs'] = getText(dom.getElementsByTagName('sleep_regular_secs')[0].childNodes)
        attrs['sleep_random_bool'] = getText(dom.getElementsByTagName('sleep_random_bool')[0].childNodes)
        attrs['sleep_module_gets'] = getText(dom.getElementsByTagName('sleep_module_gets')[0].childNodes)
                
        bot = eval('%s()' % (attrs['class']))
        bot.initialize(self.__proxies_per_proto, attrs['user'], attrs['pass'])       
        bot.set_proxies_per_proto(self.__proxies_per_proto)
        bot.set_sleep_secs(float(attrs['sleep_regular_secs']))
        bot.set_sleep_random_flag(bool(int(attrs['sleep_random_bool'])))        
        bot.set_sleep_module(int(attrs['sleep_module_gets']))
        
        self.__lambs[attrs['class']] = bot        
        
    def __load_expander(self, dom):
        
        attrs = {}
        attrs['class'] = getText(dom.getElementsByTagName('class')[0].childNodes)
        attrs['method'] = getText(dom.getElementsByTagName('method')[0].childNodes)
        
        if not attrs['class'] in self.__expanders:
            self.__expanders[attrs['class']] = {}
        python_method = 'lambs_dict["%s"].%s' % (attrs['class'],attrs['method'])
        lambs_dict = self.__lambs
        self.__expanders[attrs['class']][attrs['method']] = eval(python_method)  
        
    def __load_weigh_scale(self, dom):
        
        attrs = {}
        attrs['class'] = getText(dom.getElementsByTagName('class')[0].childNodes)
        attrs['method'] = getText(dom.getElementsByTagName('method')[0].childNodes)
        attrs['min_weight'] = getText(dom.getElementsByTagName('min_weight')[0].childNodes)
        attrs['max_weight'] = getText(dom.getElementsByTagName('max_weight')[0].childNodes)
        attrs['context'] = getText(dom.getElementsByTagName('context')[0].childNodes)
        
        if not attrs['class'] in self.__weigh_scales:
            self.__weigh_scales[attrs['class']] = {}            
        python_method = 'lambs_dict["%s"].%s' % (attrs['class'],attrs['method'])
        lambs_dict = self.__lambs
        self.__weigh_scales[attrs['class']][attrs['method']] = eval(python_method)
        
        self.__weigh_scales_params[eval(python_method)] = {}
        self.__weigh_scales_params[eval(python_method)]['min_weight'] = float(attrs['min_weight'])
        self.__weigh_scales_params[eval(python_method)]['max_weight'] = float(attrs['max_weight'])        
        self.__weigh_scales_params[eval(python_method)]['context'] = attrs['context']

    def set_weigh_scale_params(self, python_method, param, val):
        classname = python_method.split('::')[0]
        method = python_method.split('::')[1]
        python_method_func = self.__weigh_scales[classname][method]
        self.__weigh_scales_params[python_method_func][param] = val 

    def get_weigh_scale_params(self, python_method):
        return self.__weigh_scales_params[python_method]
        
    def set_proxies(self, proxies_per_proto):
        self.__proxies_per_proto = proxies_per_proto        
    
    def __iter__(self):
        for bot in self.__expanders:
            for method in self.__expanders[bot]:
                yield '%s::%s' % (bot,method)
        
    def iter_weigh_scales(self):
        for bot in self.__weigh_scales:
            for method in self.__weigh_scales[bot]:
                yield '%s::%s' % (bot,method)
        
    def iter_chatbots(self):
        for bot in self.__lambs:
            if self.__lambs[bot].is_chatbot():
                yield '%s' % (bot)
        
    def iter_bots(self):
        for bot in self.__lambs:
            yield '%s' % (bot)
        
    def get_bot_inst(self, bot):
        return self.__lambs[bot]

    def __getitem__(self, node_exp):
        class_ = node_exp.split('::')[0]
        method_ = node_exp.split('::')[1]
        ret = self.__expanders[class_][method_]
        return ret

    def get_weigh_scale(self, node_exp):
        class_ = node_exp.split('::')[0]
        method_ = node_exp.split('::')[1]
        ret = self.__weigh_scales[class_][method_]
        return ret

    
