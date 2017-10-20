
from ExomindException import ExomindException
from Utils import normalize_token

class SQLGraph:
    
    def __init__(self, name, builder_rep=None):
        if not builder_rep:
            raise ExomindException('you cannot create SQLGraph instances, use GraphBuilder instead')
        self.__name = name
        self.__rep = builder_rep
        
        self.multiedges = False    

    def nodes(self):
        return self.__rep.get_nodes(self.__name)
        
    def node_attrs(self, n=None, type=None):
        n = normalize_token(n)
        return self.__rep.get_nodes_attrs(self.__name, n, type)
        
    def edges(self, n=None):
        n = normalize_token(n)
        return self.__rep.get_edges(self.__name, n)
        
    def edge_attrs(self, n1, n2=None):
        n1 = normalize_token(n1)        
        n2 = normalize_token(n2)
        return self.__rep.get_edge_attrs(self.__name, n1, n2)
        
    def has_node(self, n):
        n = normalize_token(n)
        return self.__rep.exists_node(self.__name, n)    

    def has_node_attr(self, n, type, attr):
        n = normalize_token(n)
        return self.__rep.exists_node_attr(self.__name, n, type, attr)    

    def has_edge_attr(self, n1, n2, type, attr):
        n1 = normalize_token(n1)
        n2 = normalize_token(n2)
        return self.__rep.exists_edge_attr(self.__name, n1, n2, type, attr)    

    def add_node(self, n):
        n = normalize_token(n)
        self.__rep.add_node(self.__name, n)
        
    def add_node_attr(self, n, type, attr):
        n = normalize_token(n)
        attr = normalize_token(attr)
        if attr:
            attr = normalize_token(attr)
        self.__rep.add_node_attr(self.__name, n, type, attr)
        
    def del_node(self, n):
        n = normalize_token(n)
        self.__rep.delete_node(self.__name, n)
        
    def has_edge(self, n1, n2=None):
        n1 = normalize_token(n1)
        n2 = normalize_token(n2)
        return self.__rep.exists_edge(self.__name, n1, n2)        

    def add_edge(self, n1, n2=None):  
        n1 = normalize_token(n1)
        n2 = normalize_token(n2)
        if n2 is None:  
            if len(n1)==3:  
                n1,n2,x=n1 
            else:           
                n1,n2=n1        
        self.__rep.add_edge(self.__name, n1, n2)    
    
    def add_edge_attr(self, n1, n2, type, attr):  
        n1 = normalize_token(n1)
        n2 = normalize_token(n2)
        attr = normalize_token(attr)
        self.__rep.add_edge_attr(self.__name, n1, n2, type, attr)    
    
    def del_edge(self, n1, n2=None):
        n1 = normalize_token(n1)
        n2 = normalize_token(n2)
        if n2 is None:  
            n1,n2=n1   
        self.__rep.delete_edge(self.__name, n1, n2)
        
    def neighbors(self, n):
        n = normalize_token(n)
        for edge in self.__rep.get_edges(self.__name, n):
            yield edge[1]

    def subgraph(self, ncolection):
        name = self.__rep.get_temporary_graph()
        self.__rep.create_graph(name)
        subg = SQLGraph(name, self.__rep)
        for node in ncolection:
            if not subg.has_node(node):
                subg.add_node(node)
                for node_bis, type, attr, count in self.node_attrs(node):
                    subg.add_node_attr(node, type, attr)
            for edge in self.edges(node):
                if edge[1] in ncolection:
                    node_x = edge[1]
                    if not subg.has_node(node_x):
                        subg.add_node(node_x)
                        for node_bis, type, attr, count in self.node_attrs(node_x):
                            subg.add_node_attr(node_x, type, attr)
                    if not subg.has_edge(node, edge[1]):
                        subg.add_edge(node, edge[1])
                        for node1, node2, type, attr, count in self.edge_attrs(node, edge[1]):
                            subg.add_edge_attr(node1, node2, type, attr)

        return subg
    
    def is_directed(self):
        return True
    
    def __contains__(self, n):
        n = normalize_token(n)
        return self.__rep.exists_node(self.__name, n)
    
