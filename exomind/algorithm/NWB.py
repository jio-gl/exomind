
from exomind.Attributes import Attributes

class NWB:
    
    @classmethod
    def export_directed_unweighted(cls, graph, path):
        f = open(path, 'w')
        num_nodes = 0
        for node in graph.nodes():
            num_nodes += 1
        f.write('*Nodes %d\n' % num_nodes)
        f.write('id*string\n')
        for node in graph.nodes():
            f.write('"%s"\n' % node)
        f.write('*DirectedEdges\n')
        f.write('source*string      target*string\n')
        for edge in graph.edges():
            f.write('"%s" "%s"\n' % edge)
        f.close()        
    

    @classmethod
    def export_directed_weighted(cls, graph, path):
        f = open(path, 'w')
        num_nodes = 0
        for node in graph.nodes():
            num_nodes += 1
        f.write('*Nodes %d\n' % num_nodes)
        f.write('id*string\n')
        for node in graph.nodes():
            f.write('"%s"\n' % node)
        f.write('*DirectedEdges\n')
        f.write('source*string      target*string      weight*float\n')
        for node1, node2 in graph.edges():
            w = None
            for node1x, node2x, type, attr, count in graph.edge_attrs(node1, node2):
                if type == Attributes.WEIGHT_ATTR:
                    w = attr
            if not w:
                raise Exception('Edge %s has no attribute WEIGHT!' % (str(node1,node2)))
            f.write('"%s" "%s" %s\n' % (node1, node2, w))
        f.close()        
    

    
    
    

if __name__ == '__main__':
    pass
