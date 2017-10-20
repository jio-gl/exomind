
from Exomind import Exomind
from BlackWidow import _CRAWL_DST_DB

import sys

exomind = None
__DEBUG = False
__ascii = """
   ____
  /           ___   __  __   __
 \      \  / |===| |==\/==| |  | |\  |     |
 =\=     \/  |   | |  ||  |  ==  |\  |  ___|
  /      /\  |   | |  ||  |  __  | \ | |===|
 /      /  \  ===  |      | |  | |  \| \===/
 \                          |  |       
  =====                     |  |
                             ==
Exomind v0.2
Jose Orlicki (@ Core Security)
Copyright (c) 2008 Core Security Technologies, Core SDI Inc.
All rights reserved.

                              """
                              
__help = """     
Exomind Help:
    llh/load_lamb_herd
    gs/graphs
    g/graph <graph_name>
    del_graph <graph_name>
    fg/focus_graph [<graph_name>]
    n/node <node_name>
    dn/del_node <node_name>
    na/node_attrs <node_name>
    add_node_attr <node_name> <attr_type> <attr>
    f/focus/fn/focus_node [<node_name>]
    l/link <node_name_u> <node_name_v>
    dl/del_link <node_name_u> <node_name_v>
    la/link_attrs <node_name>
    add_link_attr <node1_name> <node2_name> <attr_type> <attr>
    ns/nodes
    ls/links [<node_name>]
    fr/focus_region/ [<region_size>]
    p/plot [<filetype>] - ps by default, png, svg, et cetera
    ib/import_basic <filepath>
    et/export_tagged <filepath>
    ae/all_expanders
    de/add_expander <expander>
    ce/clear_expanders
    es/expanders
    aw/all_weigh_scales
    dw/add_weigh_scale <weigh_scale> [<min_w_filt>] [<max_w_filt>] [<context>]
    cw/clear_weigh_scales
    ws/weigh_scales
    c/crawl [<max_nodes>] [<max_seconds>] [<continue_old_queue>] [<storage_type>] [<file>]
            - <max_nodes> and <max_seconds> have no limit by default.
            - continue_old_queue is False by default, crawling is BFS by default
            - storage_type is DST_DB (default) or DST_FILE, specify [file] if DST_FILE
    ac/all_chatbots
    cb/chatbots
    dc/add_chatbot <chatbot_name>
    cc/clear_chatbots
    ic/infiltrate_chat [<initial_msg>='hello'] [<repeat_in_secs>=3600] [<alternative_nickname>=None]
    cx/context <new_context_for_searches>
    save_cache - save search engine cache
    h/help
    e/exit
    """

__MAX_PARAMS = 10

def __init__():
    exomind = Exomind()
    
    begin_graph = 'NO_NAMER'
    begin_node = 'Alice'
    begin_node2 = 'Bob'
    try:
        exomind.drop_graph(begin_graph)
    except:
        pass
    exomind.create_graph(begin_graph)
    exomind.set_focus_graph(begin_graph)
    exomind.add_edge(begin_node, begin_node2)
    exomind.set_focus_node(begin_node)

    print
    print 'Welcome to Exomind!'
    print __ascii
    return exomind    

def start():
    pass
           

def plot(param0=None):
    if param0:
        type = param0
    else:
        type = 'ps'

    less_than_three = True
    i = 0
    for node in exomind.nodes():
        i += 1
        if i >= 2:
            less_than_three = False
            break
    if less_than_three:
        print 'Error: cannot plot graph with 0 or 1 nodes.'
    else:
        exomind.plot(type)


def graphs():
    graphs = exomind.get_graphs()
    for graph in graphs:
        print graph

def links(param0=None):
    edges = exomind.edges(param0)
    i = 0
    for edge in edges:
        print edge
        i += 1
    
    print '---'
    print 'Total number of edges: %d' % i

def nodes():
    nodes = exomind.nodes()
    i = 0
    for node in nodes:
        print '\'%s\'' % node
        i += 1
    
    print '---'
    print 'Total number of nodes: %d' % i

def link(param0=None, param1=None):
    if not param0 or not param1:
        print 'Error: command link needs 2 parameters.'  
        return
    node_u = param0
    node_v = param1
    if exomind.exists_edge(node_u, node_v):
        print 'Error: in graph "%s" edge ("%s","%s") already exists.' % (exomind.get_focus_graph(), node_u, node_v)
    else:
        if not exomind.exists_node(node_u):
            exomind.add_node(node_u)
    
        if not exomind.exists_node(node_v):
            exomind.add_node(node_v)
    
        exomind.add_edge(node_u, node_v)

def del_link(param0=None, param1=None):
    if not param0 or not param1:
        print 'Error: command del_link needs 2 parameters.'  
        return
    node_u = param0
    node_v = param1
    if not exomind.exists_edge(node_u, node_v):
        print 'Error: in graph "%s" edge ("%s","%s") does not exist.' % (exomind.get_focus_graph(), node_u, node_v)
    else:
        exomind.del_edge(node_u, node_v)

def node(param0=None):
    if not param0:
        print 'Error: command node needs 1 parameter.'  
        return
    node = param0
    if exomind.exists_node(node):
        print 'Error: in graph "%s " node with name/alias "%s" already exists.' % (exomind.get_focus_graph(), node)
    else:
        exomind.add_node(node)
    return node

def del_node(param0=None):
    if not param0:
        print 'Error: command del_node needs 1 parameter.'  
        return
    node = param0
    if not exomind.exists_node(node):
        print 'Error: in graph "%s " node with name "%s" does not exist.' % (exomind.get_focus_graph(), node)
    else:
        exomind.del_node(node)
    return node

def node_attrs(param0=None):
    if not param0:
        print 'Error: command node_attrs needs 1 parameter.'  
        return 
    node = param0
    if not exomind.exists_node(node):
        print 'Error: in graph "%s " node with name "%s" does not exist.' % (exomind.get_focus_graph(), node)
    else:            
        for attrs in exomind.node_attrs(node):
            print (attrs[1],attrs[2], attrs[3])

def add_node_attr(param0, param1, param2):
    exomind.add_node_attr(param0, param1, param2)

def link_attrs(param0=None, param1=None):
    if not param0:
        print 'Error: command link_attrs needs 1 or 2 parameters.'  
        return
    node = param0
    neigh = param1
    if param1 and not exomind.exists_edge(node, neigh):
        print 'Error: in graph "%s " edge ("%s","%s") does not exist.' % (exomind.get_focus_graph(), node, neigh)
    else:          
        if param1:  
            for attrs in exomind.edge_attrs(node, neigh):
                print (attrs[2],attrs[3], attrs[4])
        else:
            for attrs in exomind.edge_attrs(node, neigh):
                print (attrs[1],attrs[2],attrs[3], attrs[4])

def add_link_attr(param0, param1, param2, param3):
    exomind.add_edge_attr(param0, param1, param2, param3)

            

def focus_graph(param0=None):
    if not param0:
        print exomind.get_focus_graph()
    else:             
        graph_name = param0
        if not exomind.exists_graph(graph_name):
            print 'Error: graph with name "%s" does not exist.' % graph_name
        else:
            exomind.set_focus_graph(graph_name)            

def focus_node(param0=None):
    if not param0:
        print exomind.get_focus_node()
    else:
        node = param0
        if not exomind.exists_node(node):
            print 'Error: node with name "%s" does not exist.' % node
        else:
            exomind.set_focus_node(node)            


def focus_region(param0=None):
    if not param0:
        print exomind.get_focus_region()
    else:        
        int_region = int(param0)
        if int_region < 2 or int_region > 2000:
            print 'Error: focus must be between 2 and 2000.'
        else:
            exomind.set_focus_region(int_region)            


def new_graph(param0=None):
    if not param0:
        print 'Error: command new_graph needs 1 parameter.'  
    else:
        graph_name = param0
        if exomind.exists_graph(graph_name):
            print 'Error: graph with name "%s" already exists.' % graph_name
        else:
            exomind.create_graph(graph_name)        


def del_graph(param0=None):
    if not param0:
        print 'Error: command del_graph needs 1 parameter.'  
    else:
        graph_name = param0
        if not exomind.exists_graph(graph_name):
            print 'Error: graph with name "%s" does not exist.' % graph_name
        else:
            exomind.drop_graph(graph_name)        


def import_basic(param0=None):
    if not param0:
        print 'Error: command import_basic needs 1 parameter.'  
    else:
        filepath = param0
        try:
            exomind.import_basic(filepath)
        except Exception, e:
            print e

def export_tagged(param0=None):
    if not param0:
        print 'Error: command export_tagged needs 1 parameter.'  
    else:
        filepath = param0
        #try:
        exomind.export_tagged(filepath)
        #except Exception, e:
        #    print e

def all_expanders():
    try:
        for exp in exomind.all_expanders():
            print exp
    except Exception, e:
        print e

def expanders():
    try:
        for exp in exomind.expanders():
            print exp
    except Exception, e:
        print e

def add_expander(param0=None):
    if not param0:
        print 'Error: command add_expander needs 1 parameter.'  
    else:
        try:
            expander_name = param0
            exomind.add_expander(expander_name)            
        except Exception, e:
            print e               

def clear_expanders():
    try:
        exomind.clear_expanders()            
    except Exception, e:
        print e
        raise

def all_weigh_scales():
    try:
        for exp in exomind.all_weigh_scales():
            print exp
    except Exception, e:
        print e

def weigh_scales():
    try:
        for exp in exomind.weigh_scales():
            print exp
    except Exception, e:
        print e

def add_weigh_scale(param0=None, param1=None, param2=None, param3=None):
    if not param0:
        print 'Error: command add_weigh_scale needs at least 1 parameter.'  
    else:
        try:
            weigh_scale_name = param0
            exomind.add_weigh_scale(weigh_scale_name, param1, param2, param3)            
        except Exception, e:
            print e               

def clear_weigh_scales():
    try:
        exomind.clear_weigh_scales()            
    except Exception, e:
        print e
        raise

def crawl(param0=None, param1=None, param2=None, param3=None, param4=None):
#        if not param0 or not param1:
#            print 'Error: command crawl needs 2 parameters.'  
    if param0:
        size = int(param0)
    else:
        size = 999999999
    if param1:
        duration_secs = float(param1)
    else:
        duration_secs = 999999999.0
    if param2:
        if param2 == 'True':
            continue_old = True
        elif param2 == 'False':
            continue_old = False
        else:
            raise Exception('bad boolean parameter: %s' % param2)
    else:
        continue_old = False 
    if param3:
        dst_type = param3
    else:
        dst_type = _CRAWL_DST_DB
    if param4:
        output_file = param4
    else:
        output_file = None

    #try:
    exomind.crawl(size, duration_secs, continue_old, dst_type, output_file)
    #except Exception, e:
    #    print 'Error: ' + str(e)
    #    raise e

def all_chatbots():
    try:
        for exp in exomind.all_chatbots():
            print exp
    except Exception, e:
        print e


def add_chatbot( param0 ): 
    if not param0:
        print 'Error: command add_chatbot needs 1 parameter.'  
    else:
        try:
            chatbot_name = param0
            exomind.add_chatbot(chatbot_name)            
        except Exception, e:
            print e               

def chatbots():
    try:
        for cb in exomind.chatbots():
            print cb
    except Exception, e:
        print e


def clear_chatbots():
    try:
        exomind.clear_chatbots()            
    except Exception, e:
        print e
        raise

# if no showname is given, user the focus_node nickname on chats
def infiltrate_chat( initial_msg='hello', repeat_in_secs=3600, showname = None, use_se_distances=True):
    exomind.infiltrate_chat(initial_msg, repeat_in_secs, showname)

def context(param0=None):
    exomind.set_context(param0)

def help():
    print __help
    #return __help

def load_lamb_herd():
    exomind.load_lamb_herd()

def save_cache():
    exomind.save_cache()

# method aliases
gs = graphs
g  = graph = new_graph
fg = focus_graph
n  = node
dn = del_node
na = node_attrs
f  = focus = fn = focus_node
l  = link
dl = del_link
la = link_attrs
ns = nodes
ls = links
fr = focus_region
p  = plot
ib = import_basic
et = export_tagged
ae = all_expanders
de = add_expander
ce = clear_expanders
es = expanders
aw = all_weigh_scales
dw = add_weigh_scale
cw = clear_weigh_scales
ws = weigh_scales
c  = crawl
ac = all_chatbots
cb = chatbots
dc = add_chatbot
cc = clear_chatbots
ic = infiltrate_chat
cx = context
h  = help
llh = load_lamb_herd


exomind = __init__()

    
    
    

