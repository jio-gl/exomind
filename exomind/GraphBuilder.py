
from GraphBuilderRep import GraphBuilderRep
from SQLGraph import SQLGraph

class GraphBuilder:
    
    def __init__(self, db_user, db_passwd):
        self.__rep = GraphBuilderRep(db_user, db_passwd)
        
    def __contains__(self, graph_name):
        return graph_name in self.__rep
    
    def create_graph(self, graph_name):
        self.__rep.create_graph(graph_name)
        
    def drop_graph(self, graph_name):
        self.__rep.drop_graph(graph_name)
        
    def __getitem__(self, graph_name):
        return SQLGraph(graph_name, self.__rep)
    
    def __iter__(self):
        return self.__rep.get_graphs(False)