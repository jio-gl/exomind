
from ForeignAffairs import ForeignAffairs
from GraphBuilder import *
from QueueBuilder import *
from ExomindException import *
from LambHerd.Lambs import Lambs 
from BlackWidow import BlackWidow, _CRAWL_BFS, _CRAWL_DFS, _CRAWL_DST_DB, _CRAWL_DST_FILE
from Utils import getText, normalize_token
from Utils import normalize_token
from Attributes import Attributes
from LambHerd.Bots.Dino import Dino
from LambHerd.Bots.Bag import Bag
from initial_configuration import *

import time
import os.path

# only for plotting
try:
	import pygraphviz
except:
	pass

import math, os
import xml.dom.minidom
import os.path

class Exomind:
    
    __focus_graph = None
    __focus_node = None
    __focus_region = 50
    __context = ''
    
    def __init__(self, proxies_per_proto={}, debug=False):
        
        self.__load_configuration()
        
        self.__importer = ForeignAffairs(self)
        self.__graphs = GraphBuilder(self.__db_user, self.__db_passwd)
        self.__queues = QueueBuilder(self.__db_user, self.__db_passwd)

        self.__expanders = []
        self.__weigh_scales = []
        self.__chatbots = []
        
    def load_lamb_herd(self):
    	self.__lambs = Lambs(self.__sleep_failure, self.__proxies_per_proto)
    
    def __create_first_configuration(self):
    	print 'Creating initial configuration...'
    	home_path = os.path.expanduser('~')
    	conf_path = home_path + '/.exomind/'
    	os.mkdir(conf_path)
    	open(conf_path + 'exomind.xml','w').write(initial_exomind)
    	open(conf_path + 'bots.xml','w').write(initial_bots)
    	open(conf_path + 'expanders.xml','w').write(initial_expanders)
    	open(conf_path + 'weigh_scales.xml','w').write(initial_weigh_scales)
    	
    
    def __load_configuration(self):
        print
        path =  '/.exomind/exomind.xml'
        try:
        	full_path = os.path.expanduser('~') + path
        	f = open(full_path)
        except Exception, e:
        	try:
        	   raise Exception('bla')	
        	   #full_path = '.' + path
        	   #f = open(full_path)
        	except Exception, e:
        	   self.__create_first_configuration()
        	   self.__load_configuration()
        	   return           	   
         	   #raise e
            
        dom = xml.dom.minidom.parseString(f.read())
        f.close()

        attrs = {}
        
        attrs['database_user'] = getText(dom.getElementsByTagName('database_user')[0].childNodes)
        attrs['database_password'] = getText(dom.getElementsByTagName('database_password')[0].childNodes)
        attrs['http_proxy'] = getText(dom.getElementsByTagName('http_proxy')[0].childNodes)
        attrs['https_proxy'] = getText(dom.getElementsByTagName('https_proxy')[0].childNodes)
        attrs['focus_region_size'] = getText(dom.getElementsByTagName('focus_region_size')[0].childNodes)
        attrs['sleep_secs_on_failure'] = getText(dom.getElementsByTagName('sleep_secs_on_failure')[0].childNodes)
        attrs['crawl_batch_size'] = getText(dom.getElementsByTagName('crawl_batch_size')[0].childNodes)
        attrs['ps_viewer'] = getText(dom.getElementsByTagName('ps_viewer')[0].childNodes)

        self.__db_user = attrs['database_user'] 
        self.__db_passwd = attrs['database_password']
        proxies_per_proto = {}
        if attrs['http_proxy'] != '':
            proxies_per_proto['http'] = attrs['http_proxy']
        if attrs['https_proxy'] != '': 
            proxies_per_proto['https'] = attrs['https_proxy']
        self.__proxies_per_proto = proxies_per_proto
        self.__focus_region = int(attrs['focus_region_size'])
        self.__sleep_failure = float(attrs['sleep_secs_on_failure'])
        self.__crawl_batch_size = int(attrs['crawl_batch_size'])
        self.__sleep_secs_on_failure = float(attrs['sleep_secs_on_failure'])
        self.__ps_viewer = attrs['ps_viewer']
        
    def exists_graph(self, name):
        return name in self.__graphs
    
    def create_graph(self, graph_name, directed=True, self_loops=False, multi_edges=True):
        if directed:
            self.__graphs.create_graph(graph_name)
        else:
            raise ExomindException('undirected graphs not implemented yet')
        if not self.__focus_graph:
            self.__focus_graph = graph_name 
	
    def drop_graph(self, graph_name):
	   self.__graphs.drop_graph(graph_name)

    def set_focus_graph(self, name):
        self.__focus_graph = name
    	# len() > 0
    	non_empty = False
        if not self.exists_node(self.__focus_node):
            self.__focus_node = None
            for n in self.__graphs[self.__focus_graph].nodes():
                self.__focus_node = n
                break
        
    def get_focus_graph(self):
        return self.__focus_graph
        
    def exists_node(self, node):
        return self.__graphs[self.__focus_graph].has_node(node)
    
    def add_node(self, node):
        self.__graphs[self.__focus_graph].add_node(node)
        if not self.__focus_node:
            self.__focus_node = node 
        
    def del_node(self, node):
        self.__graphs[self.__focus_graph].del_node(node)
        if self.__focus_node == node:
            self.__focus_node = None 
        
    def set_focus_node(self, node):
        self.__focus_node = normalize_token(node)
        
    def get_focus_node(self):
        return self.__focus_node
        
    def set_focus_region(self, int_region):
        self.__focus_region = int_region
        
    def get_focus_region(self):
        return self.__focus_region
        
    def exists_edge(self, u, v=None):
        return self.__graphs[self.__focus_graph].has_edge(u, v)
    
    def add_edge(self, u, v=None):
        self.__graphs[self.__focus_graph].add_edge(u, v)
        if not self.__focus_node:
            self.__focus_node = u 
        
    def del_edge(self, u, v=None):
        self.__graphs[self.__focus_graph].del_edge(u, v)
        
    def nodes(self):
        return self.__graphs[self.__focus_graph].nodes()
        
    def node_attrs(self, node):
        return self.__graphs[self.__focus_graph].node_attrs(node)
        
    def add_node_attr(self, node, type, attr):
        return self.__graphs[self.__focus_graph].add_node_attr(node, type, attr)
        
    def edges(self, node=None):
        return self.__graphs[self.__focus_graph].edges(node)
        
    def edge_attrs(self, n1, n2=None):
        return self.__graphs[self.__focus_graph].edge_attrs(n1, n2)
        
    def add_edge_attr(self, node1, node2, type, attr):
        return self.__graphs[self.__focus_graph].add_edge_attr(node1, node2, type, attr)
        
    def get_graphs(self):
        for graph_name in self.__graphs:
            yield graph_name
    
    def is_directed(self):
        return self.__graphs[self.__focus_graph].is_directed()
    
    def __bfs(self):        
        focus_graph = self.__graphs[self.__focus_graph]
        queue = [self.__focus_node]
        region = set([self.__focus_node])
        visited = []
        while len(queue) != 0 and len(region) < self.__focus_region:
            node = queue.pop(0)
            visited.append(node)            
            neighs = focus_graph.neighbors(node)
            new_nodes = []
            i = 0
            for neigh in neighs:
                new_nodes.append(neigh)
                i += 1
                if i >= self.__focus_region - len(region):
                    break
                if not neigh in visited and not neigh in queue:
                    queue.append(neigh)
            region = region.union(set(new_nodes))
        return focus_graph.subgraph(region)
    
    
    def __gen_dot(self):
        
        focus_graph = self.__bfs()

        g = pygraphviz.AGraph(strict=True,directed=focus_graph.is_directed())        
        g.graph_attr['outputorder']="edgesfirst"
        
        nodes = focus_graph.nodes()
        for n in nodes:
            g.add_node(n)

        g.node_attr['style']='filled'
        g.node_attr['shape']='circle'
        g.node_attr['fixedsize']='true'
        g.node_attr['fontcolor']= '#444444' #'#448800' #'#008800'
        g.node_attr['fontsize']= '%f' % (20.0/math.log(len(g.nodes())+2,2))
      
        node_weight = {}
        node_color_dict = {}
        for i in g.nodes():
            n=g.get_node(i)
            node_color = None
            for node, type, attr, count in focus_graph.node_attrs(n):
                if type == Attributes.WEIGHT_ATTR:
                    node_weight[n] = float(attr)
                new_color = Attributes.choose_node_color(type)
                #	node_color = new_color
                if new_color:
                	node_color = new_color
                	node_color_dict[node] = new_color    
            color = 128
            if color < 0:
                color = 0
            if color > 256:
                color = 256
            if node_color:
                n.attr['fillcolor']=node_color
            else:
                n.attr['fillcolor']='#eeeeee'
            # if ofuscated, print smaller
            if n.endswith('='):
                n.attr['fontsize']='%f' % (8.0/math.log(len(g.nodes())+2,2))
            max_w = 1.0
            if i in node_weight:
                size = float(node_weight[i])/max_w+0.35
            else:
                size = 0.5
            if size < 0.30:
                size = 0.30
            if n == self.__focus_node:
                size *= 2
                n.attr['fillcolor']='#eeeeee'  #'#ffffff' #"#22bbbb"
            n.attr['height']="%f"%(float(size)/math.log(len(g.nodes())+1,2))
            n.attr['width']="%f"%(float(size)/math.log(len(g.nodes())+1,2))

            
        for e in focus_graph.edges():
            edge_weight = None
            edge_color = None
            for node1, node2, type, attr, count in focus_graph.edge_attrs(e[0],e[1]):
                if type == Attributes.WEIGHT_ATTR:
                    edge_weight = float(attr)
                if not edge_color:
      	            if e[1] in node_color_dict:
      	            	edge_color = node_color_dict[e[1]]

            g.add_edge(e[0],e[1])
            e2 = g.get_edge(e[0],e[1])
            
            if edge_weight:
                e = (e[0],e[1], edge_weight)
                #e = (e[0],e[1], 1)
            else:
                e = (e[0],e[1], 1)
            width = e[2]*40.0
            if width < 0.0:
                width = 0.0
            if width > 10.0:
                width = 10.0
            e2.attr['style'] = "setlinewidth(%f)" % ((10.0-width)/math.log(len(g.nodes()),2))
            color = e[2]*256
            if color < 0:
                color = 0
            if color > 150:
                color = 150

            if edge_color:
                e2.attr['color'] = edge_color
            else:
                e2.attr['color'] = "#22bb00" #"#000000"
            
            e2.attr['label'] = ""
            e2.attr['arrowsize'] = "%f"  % (((10-width)/math.log(len(g.nodes()),2)) / 3.5)
            e2.attr['weight'] = "0.9"
      
        g.write("./plot.dot") # write to simple.dot
        time.sleep(0.5)
        
    def __gen_view_image(self, type='ps'):
        if type=='ps':
            os.system('neato ./plot.dot -o ./plot.%s -T%s &> /dev/null' % (type,type) + ';sleep 0.1; %s ./plot.%s &> /dev/null' % (self.__ps_viewer,type))        
            print "Wrote ./plot.%s" % type
            print "Viewing ./plot.%s with %s" % (type,self.__ps_viewer)
        elif type=='png' or type=='jpg':
            os.system('neato ./plot.dot -o ./plot.%s -T%s &> /dev/null' % (type,type) + ';sleep 0.1; eog ./plot.%s &> /dev/null' % type)        
            print "Wrote ./plot.%s" % type
            print "Viewing ./plot.%s with eog" % type
        elif type=='svg':
            os.system('neato ./plot.dot -o ./plot.%s -T%s &> /dev/null' % (type,type) + ';sleep 0.1; firefox ./plot.%s &> /dev/null' % type)        
            print "Wrote ./plot.%s" % type
 #           os.system(';eog ./plot.%s &> /dev/null' % type)        
            print "Viewing ./plot.%s with eog" % type
        else:
            raise Exception('unsupported image file: %s' % type)
             

    def plot(self, type='ps'):
        self.__gen_dot()
        self.__gen_view_image(type)
        
         
    def import_basic(self, filepath):
        self.__importer.import_basic(filepath)

    def export_tagged(self, filepath):
        self.__importer.export_tagged(filepath)

    def all_expanders(self):
        for node_exp in self.__lambs:
            yield node_exp
        
    def expanders(self):
        for node_exp in self.__expanders:
            yield node_exp
        
    def add_expander(self, exp_name):
        self.__expanders.append(exp_name)
        
    def clear_expanders(self):
        self.__expanders = []
        
    def all_weigh_scales(self):
        for node_exp in self.__lambs.iter_weigh_scales():
            yield node_exp
        
    def weigh_scales(self):
        for node_exp in self.__weigh_scales:
            yield node_exp
        
    def add_weigh_scale(self, exp_name, min_w=None, max_w=None, context=None):
        self.__weigh_scales.append((exp_name, min_w, max_w, context))
        
    def clear_weigh_scales(self):
        self.__weigh_scales = []
        
    def crawl(self, size=999999999, 
                  duration_secs=999999999.0, 
                  continue_old=False, 
                  crawl_dst=_CRAWL_DST_DB,
                  output_file=None,
                  type='BFS'):
        
        if len(self.__expanders) == 0:
            raise ExomindException('expander list is empty.')
        if not self.__focus_node:
            raise ExomindException('no focus_node set.')
        graph = self.__graphs[self.__focus_graph]
        seeds = [self.get_focus_node()]
        node_exps = []
        for node_exp_name in self.__expanders:
            node_exps.append(self.__lambs[node_exp_name])
        
        #self.__queues.create_queue(self.get_focus_node())
        queue = self.__queues.get_queue(self.get_focus_node(), not continue_old, False)
             
        visited_set_name = self.get_focus_node() + '__visited__'
        # visited queue/set has and INDEX in the database (True)
        visited_set = self.__queues.get_queue(visited_set_name, not continue_old, True)
        
        weigh_scales_dict = {}
        for (weigh_scale, min_w, max_w, context) in self.__weigh_scales:
            # set LambHers weigh_scale params
            if min_w:
                self.__lambs.set_weigh_scale_params(weigh_scale, 'min_weight', min_w)
            if max_w:
                self.__lambs.set_weigh_scale_params(weigh_scale, 'max_weight', max_w)
            if context:
                self.__lambs.set_weigh_scale_params(weigh_scale, 'context', context)
            classname = weigh_scale.split('::')[0] 
            method = weigh_scale.split('::')[1]
            weigh_scales_dict[self.__lambs.get_weigh_scale(weigh_scale)] = self.__lambs.get_weigh_scale_params(self.__lambs.get_weigh_scale(weigh_scale)) 
        
        if type == 'BFS':
            crawler = BlackWidow(graph, queue, visited_set, seeds, node_exps, weigh_scales_dict, _CRAWL_BFS, self.__crawl_batch_size)
        elif type == 'DFS':
            crawler = BlackWidow(graph, queue, visited_set, seeds, node_exps, weigh_scales_dict, _CRAWL_DFS, self.__crawl_batch_size)
        else:
            raise Exception('unsupported crawl type: %s' % type)

        crawler.set_continue_old(continue_old)
        crawler.set_crawl_dst(crawl_dst)
        crawler.set_output_file(output_file)
        crawler.set_sleep_failure(self.__sleep_secs_on_failure)
        crawler.crawl(size, duration_secs)

    def get_weigh_scale(self):
        return self.__weigh_scale

    def get_weigh_scale_min(self):
        return self.__weigh_scale_inst.get_filtering_min()
    
    def get_weigh_scale_max(self):
        return self.__weigh_scale_inst.get_filtering_max()

    def set_weigh_scale(self, wsbool):
        self.__weigh_scale = wsbool

    def set_weigh_scale_min(self, wsmin):
        self.__weigh_scale_inst.set_filtering_min(wsmin)        
    
    def set_weigh_scale_max(self, wsmax):
        self.__weigh_scale_inst.set_filtering_max(wsmax)

    def get_graph_instance(self, graphname):
        return self.__graphs[graphname]
    
    def all_chatbots(self):
        for chatbot in self.__lambs.iter_chatbots():
            yield chatbot

    def add_chatbot(self, cb_name):
        self.__chatbots.append(cb_name)
        
    def chatbots(self):
        for cb in self.__chatbots:
            yield cb
        
    def clear_chatbots(self):
        self.__chatbots = []

    def __create_vocabulary_profile(self, node):
		freq_pairs = []
		for node, type, attr, count in self.node_attrs(node):
			if type == Attributes.TAG_ATTR:
				freq_pairs.append((attr,count))
		bag = Bag(freq_pairs)
		return bag
       
    def infiltrate_chat(self, initial_msg='hello', repeat_in_secs = None, nickname=None, query_chat_dists=True):
        
        # 0 - Agregarle al MSNBot la opcion de quit/stop!!! DONE
        
        # 1 - Asumir que solo anda el MSNBot, no usar para THREADS todavia!!! DONE 
        
        repeat_in_secs = int(repeat_in_secs)
        
        bot = self.__lambs.get_bot_inst('MSNBot')
        bot.set_debug(False)
        
        # 2 - Chequear si el nodo tiene mail de hotmail.
        
        n = self.__focus_node
        g = self.__graphs[self.__focus_graph]
        if not g.has_node(n):
            print 'Error: focus_node is not from the focus_graph!!!'
            return
        
        # IF IT HAS MORE THAN ONE MSN MAIL MAYBE WE SHOULD USE THREAD FOR THAT TO START WITH.
        # check if focus_node has hotmail mail.
        has_msn_mail, msn_mail = False, None
        for node, type, attr, count in g.node_attrs(n):
            if type == Attributes.EMAIL_ATTR:
                if bot.is_msn_email(attr):
                    has_msn_mail = True
            
        if not has_msn_mail and not nickname:
            print 'Warning: focus_node "%s" has not MSN email!' % n
            print 'Do you proceed? Y/n'
            input = raw_input()
            if 'n' in input.strip() or 'N' in input.strip():
                return            
        
        # 3 - Chequear si el nodo esta online.         
#        if has_msn_mail:
#            # is online?
#            is_online = bot.
#            print 'Warning: focus_node "%s" has not MSN email!' % n
#            print 'Do you proceed? Y/n'
#            input = raw_input()
#            if 'n' in input.strip() or 'N' in input.strip():
#                return            
        
        # 4 - Si no esta online, conectarse con el nick de la base o el showname y
        # agarrar los TAGs del nodo y meterlos como signature del Dino.
        if nickname:
            use_nickname = nickname
        else:
            use_nickname = n
        # build vocabulary impersonator
        voc_profile = self.__create_vocabulary_profile(n)
        dino = Dino(False)
        voc_translator = lambda text : dino.translate(text,voc_profile)
        bot.connect(use_nickname, query_chat_dists, voc_translator)
        
        # 5 - Agregar a todos los vecinos que tengan hotmail!
        contacts = []
        for node, neigh in g.edges(n):
            neigh_has_msn_mail, neigh_msn_mail = False, None
            for node_bis, type, attr, count in g.node_attrs(neigh):
                if type == Attributes.EMAIL_ATTR:
                    if bot.is_msn_email(attr):
                        neigh_has_msn_mail, neigh_msn_mail = True, attr
            if neigh_has_msn_mail:
                print '(Exomind) neighbor "%s" has msn mail "%s" adding to possible contact list.' % (neigh, neigh_msn_mail)
                bot.add_contact(neigh_msn_mail)
                contacts.append(neigh_msn_mail)

        if len(contacts) == 0:
            print 'Warning: focus_node "%s" has no possible contacts on the graph!' % n
            print 'Do you proceed? Y/n'
            input = raw_input()
            if 'n' in input.strip() or 'N' in input.strip():
                return            
        
        # 6 - Mandar mensajes iniciales a los vecinos!
        print '(Exomind) Sending initial messages to all possible contacts.'
        bot.set_first_input(contacts, [initial_msg]*len(contacts), repeat_in_secs)
        
        # 7 - Dejar corrriendo el chatbot, opcion quit?, y ver lo de molestar cada X tiempo.
        print '(Exomind) Starting chatbot loop.'
        bot.start_chatting()
        
    def set_context(self, cx):
        try:
            self.__lambs.get_bot_inst('SearchEngineBot').set_context(cx)            
        except:
            print 'Error: SearchEngineBot not included in src/bots.xml'

    def save_cache(self):
    	for botname in self.__lambs.iter_bots():
    		bot = self.__lambs.get_bot_inst(botname)
    		bot.save_cache()
    		
