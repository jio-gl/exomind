
import cgi
from exomind.Attributes import Attributes

class GraphML:

    __start = '''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
  http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">

  <!-- prefuse GraphML Writer | Mon Jul 02 11:39:43 EDT 2007 -->
  <!-- This writer works properly now. But since the source -->
  <!-- xgmml file has empty labels on every edge, the prefuse -->
  <!-- GraphML Writer generates label attribute without any value -->
  <!-- cross all edges. Have to manually remove those attributes -->
  <!-- from the file. -->
  <key id="label" for="node" attr.name="label" attr.type="string"/>
  <key id="id" for="node" attr.name="id" attr.type="string"/>
'''

    __start_directed = '''
  <graph edgedefault="directed">            
'''

    __end_directed = '''
  </graph>'''
    __end = '''
</graphml>        
        '''

    
    @classmethod
    def export_directed_unweighted(cls, graph, path):
        f = open(path, 'w')        
        f.write(cls.__start)        
        f.write(cls.__start_directed)
        node_xml = '''
    <node id="%s">
        <data key="label">%s</data>
    </node>'''
        for node in graph.nodes():
            node_esc = cgi.escape(node).replace(' ','_')
            f.write(node_xml % (node_esc, node_esc))            
            
        edge_xml = '''
    <edge id="%s" source="%s" target="%s">
    </edge>'''
        id = 0
        for edge in graph.edges():            
            node1_esc = cgi.escape(edge[0]).replace(' ','_')
            node2_esc = cgi.escape(edge[1]).replace(' ','_')            
            f.write(edge_xml % ('e%d'%id, node1_esc, node2_esc))
            id += 1
            
        f.write(cls.__end_directed)
        f.write(cls.__end)
        f.close()        

    @classmethod
    def export_directed_weighted(cls, graph, path):
        f = open(path, 'w')     
        extra = '''  <key id="weight" for="edge" attr.name="weight" attr.type="string"/>
        '''   
        f.write(cls.__start + extra)        
        f.write(cls.__start_directed)
        node_xml = '''
    <node id="%s">
        <data key="label">%s</data>
    </node>'''
        for node in graph.nodes():
            node_esc = cgi.escape(node).replace(' ', '_')
            f.write(node_xml % (node_esc, node_esc))            
            
        edge_xml = '''
    <edge id="%s" source="%s" target="%s">
          <data key="weight">%s</data>
    </edge>'''
        id = 0
        for node1, node2 in graph.edges():
            w = None
            for node1x, node2x, type, attr, count in graph.edge_attrs(node1, node2):
                if type == Attributes.WEIGHT_ATTR:
                    w = attr
            if not w:
                raise Exception('Edge %s has no attribute WEIGHT!' % (str(node1,node2)))
            node1_esc = cgi.escape(node1).replace(' ','_')
            node2_esc = cgi.escape(node2).replace(' ','_')            
            f.write(edge_xml % ('e%d'%id, node1_esc, node2_esc, w))
            id += 1
            
        f.write(cls.__end_directed)
        f.write(cls.__end)
        f.close()        

