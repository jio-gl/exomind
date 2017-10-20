
from ExomindException import ExomindException
from CallBatch import *
from Attributes import Attributes
from LambHerd.Bots.GraphBot import GraphBot


import sys, traceback
import time

_CRAWL_BFS        = 'BFS'
_CRAWL_DFS        = 'DFS'
_CRAWL_DST_DB     = 'DST_DB'
_CRAWL_DST_FILE   = 'DST_FILE'

class BlackWidow:    
    
    
    def __init__(self, graph, queue, visited_set, seeds, node_expanders, weigh_scales, crawl_type=_CRAWL_BFS, batch_size=8):
        self.__graph = graph
        self.__queue = queue
        self.__visited_set = visited_set
        self.__seeds = seeds
        self.__expanders = node_expanders
        self.__type = crawl_type
        self.__weigh_scales = weigh_scales
        #self.__weigh_scale = weigh_scale        
        
        self.__sleep_failure = 20.0
        self.__batch_size = batch_size
        self.__sleep_count = 0
        self.__crawl_dst = _CRAWL_DST_DB
        self.__output_filepath = None
    
    def set_crawl_dst(self, crawl_dst):
        self.__crawl_dst = crawl_dst
        
    def set_continue_old(self, continue_old):
        self.__continue_old = continue_old
        
    def set_output_file(self, filepath):
        self.__output_filepath = filepath
        
    def set_sleep_failure(self, secs):
        self.__sleep_failure = secs
    
    def __lifo_pop(self, stack):
        return stack.pop('LIFO')

    def __fifo_pop(self, stack):
        return stack.pop('FIFO')

    def __lifo_retrieve(self, stack, item):
        stack.unpop(item, 'LIFO')        
        return stack

    def __fifo_retrieve(self, stack, item):
        stack.unpop(item, 'FIFO')
        return stack
    
    def alias_sort(self, alias1, alias2):
        if '@' in alias1 and not '@' in alias2:
            return 1 
        if not '@' in alias1 and '@' in alias2:
            return -1 
        return len(alias2) - len(alias1) 
    
    def crawl(self, size, duration_secs):
        '''
        size : numbers if nodes you want to expand.
        duration_secs : is the maximum duration of the crawling, measured in seconds.
        '''

        # restart output file if continue_old flag is OFF.
        if not self.__continue_old and self.__output_filepath:
            f = open(self.__output_filepath, 'w')
            f.close()

        start_time = time.time()
        seeds = self.__seeds
        max_nodes = size
        if self.__type == _CRAWL_BFS:
            mode = 'BFS'
        elif self.__type == _CRAWL_DFS:
            mode = 'DFS'
        else:
            raise ExomindException('unknown crawl type: %s' % self.__type)
        
        failures = 0        
        if mode=='BFS':
            pop = self.__fifo_pop
            push_back = self.__fifo_retrieve
        elif mode=='DFS':
            pop = self.__lifo_pop
            push_back = self.__lifo_retrieve
        
        stack = self.__queue
        visited = self.__visited_set
        for seed in seeds:
            alias_attrs = self.__graph.node_attrs(seed,Attributes.ALIAS_ATTR)
            alias_attrs = list(set(map(lambda x:x[2], alias_attrs)))
            stack.push('|'.join(alias_attrs))                   
         
        while len(visited) < max_nodes and len(stack) > 0:
            # use special pop operation
            print '(blackwidow crawler) expanded/desired/stack : %d/%d/%d' % (len(visited),max_nodes,len(stack))
            
            nodes = []
            for i in range(min(self.__batch_size, max_nodes - len(visited))):
                if len(stack) == 0:
                    break
                node = pop(stack)
                if not node in visited:
                    visited.push(node)              
                    nodes.append(node)
                else:
                    continue
                        
            if time.time() - start_time > duration_secs:
                break
            else:
                print '%f seconds left.' % (duration_secs - time.time() + start_time)
            
            try:                
                batch_funs, batch_params = [], []
                for expander in self.__expanders:
                    for aliases in nodes:
                        batch_funs.append(expander)
                        node = aliases.split('|')[0]
                        alias_attrs = aliases.split('|')
                        alias_attrs.sort(self.alias_sort)
                        batch_params.append((alias_attrs, self.__graph))                       
                # the number of threads will be len(expanders) * batch_size 
                call_batch = CallBatch(batch_funs, batch_params, len(batch_funs))                
                ret_vals = call_batch.run()
                
                for (expander_fun, node), val in ret_vals.iteritems():
                    node = node.split('|')[0]
                    # weigh and filter
                    for weigh_scale in self.__weigh_scales:
                        val = weigh_scale(val, self.__weigh_scales[weigh_scale], node)
                    if self.__crawl_dst == _CRAWL_DST_DB:
                        self.__add_data_basic(max_nodes, stack, visited, node, val[0], val[1], val[2])
                    elif self.__crawl_dst == _CRAWL_DST_FILE:
                        self.__add_data_file(max_nodes, stack, visited, node, val[0], val[1], val[2])

                
            except Exception, e:
                failures += 1
                traceback.print_exc(file=sys.stdout)
                print str(e)
                print 'FAILURE: #%d expanding node #%d people' % (failures, len(visited)+1)
#                raise e

                print 'sleep %f seconds after failure' % self.__sleep_failure
                time.sleep(self.__sleep_failure)
                for node in nodes:
                    stack = push_back(stack, node)          
                    visited.pop('LIFO')
                continue      
            

        print '(blackwidow crawler) expanded/desired/stack : %d/%d/%d' % (len(visited),max_nodes,len(stack))        
                
        self.__queue.drop()
        self.__visited_set.drop()
                   
    def __add_data_basic(self, max_nodes, stack, visited, node, final_self_attrs, final_node_dict, final_link_dict):
        for type, attr in final_self_attrs:
            print '(adding node attr) node: %s | type: %s | attr: %s' % (node, type, attr)
            self.__graph.add_node_attr(node, type, attr)
        
        # ugly hack ot decrypt ofuscated names and stack them.
        if GraphBot.passw != '' and len(visited) > 1:
            node = GraphBot.encrypt(node)           
            if not self.__graph.has_node(node):     
                print '(adding OFUSCATED node) node: %s' % (node)
                self.__graph.add_node(node)
            
        for neigh, attrs in final_node_dict.iteritems():
            
            if neigh.startswith('__INVERSE__'):
                neigh = neigh.replace('__INVERSE__', '')
                _inverse = True
            else:
                _inverse = False
            if neigh != node: # and neigh.lower() != node.lower():
                neigh_alias_attrs = map(lambda x: x[1], filter(lambda x: x[0] == Attributes.ALIAS_ATTR, attrs))
                neigh_alias_attrs.sort(self.alias_sort)
                neigh = neigh_alias_attrs[0]
                if not self.__graph.has_node(neigh):
                    print '(adding node) node: %s' % (neigh)
                    self.__graph.add_node(neigh)
                
                for type, val in attrs:
                    print '(adding node attr) node: %s | type: %s | attr: %s' % (neigh, type, val)
                    self.__graph.add_node_attr(neigh, type, val)

                # hack to include inverse edges
                if not _inverse:
                    node1, node2 = node, neigh
                else:
                    node1, node2 = neigh, node
                
                if not self.__graph.has_edge(node1, node2):
                    print '(adding edge) node1: %s | node2: %s' % (node1, node2)
                    self.__graph.add_edge(node1, node2)
                
                if node2 in final_link_dict:
                    for type, val in final_link_dict[node2]:
                        print '(adding edge attr) node1: %s | node2: %s | type: %s | attr: %s' % (node1, node2, type, val)
                        self.__graph.add_edge_attr(node1, node2, type, val)

                neigh_alias_attrs = self.__graph.node_attrs(neigh, Attributes.ALIAS_ATTR)
                neigh_alias_attrs = list(set(map(lambda x: x[2], neigh_alias_attrs)))                
                if not neigh in neigh_alias_attrs:
                    neigh_alias_attrs.append(neigh)
                    
                # ugly hack ot decrypt ofuscated names and stack them.
                if GraphBot.passw != '':
                    neigh_alias_attrs = map(GraphBot.decrypt, neigh_alias_attrs)
                                        
                neigh_alias_attrs.sort(self.alias_sort)
                neigh = '|'.join(neigh_alias_attrs)         
                if not neigh in visited and len(visited) <= max_nodes:
                    stack.push(neigh)



                    
    def __add_data_file(self, max_nodes, stack, visited, node, final_self_attrs, final_node_dict, final_link_dict):
        '''
        Save information from expanded node to a file (self.__output_filepath).
        Save only the tagged graph.
        '''
        f = open(self.__output_filepath, 'aw')
        for neigh, attrs in final_node_dict.iteritems():
            if neigh != node:
                tags = []
                
                if neigh in final_link_dict:
                    for type, val in final_link_dict[neigh]:
                        if type == Attributes.TAG_ATTR:
                            print '(adding edge attr) node1: %s | node2: %s | type: %s | attr: %s' % (node, neigh, type, val)
                            tags.append(val)
                            
                # write to file.                
                f.write('%s\t\t%s\t\t%s\n' % (node, neigh, '|'.join(tags)))

                neigh_alias_attrs = self.__graph.node_attrs(neigh, Attributes.ALIAS_ATTR)
                neigh_alias_attrs = list(set(map(lambda x: x[2], neigh_alias_attrs)))
                if not neigh in neigh_alias_attrs:
                    neigh_alias_attrs.append(neigh)
                neigh_alias_attrs.sort(self.alias_sort)
                neigh = '|'.join(neigh_alias_attrs)         
                if not neigh in visited and len(visited) <= max_nodes:
                    stack.push(neigh)
        f.close()
