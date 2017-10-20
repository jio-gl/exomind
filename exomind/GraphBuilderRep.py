from Utils import to_sql_token

from Attributes import Attributes

import MySQLdb

import time, base64, md5

class GraphBuilderRep:
    
    __temp_prefix = '__temp__'

    def __table(self, name):
        #return name.replace('\t',' ').replace(' ','_').replace('-','_')
        return to_sql_token(name)
    
    def __init__(self, db_user, db_passwd):
        
        self.__db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_passwd)
        cursor = self.__db.cursor()        
        cursor.execute("CREATE DATABASE IF NOT EXISTS exomind")
        cursor.execute("USE exomind")
        self.__cursor = cursor

        # graphs tables
        statement1= """        
        CREATE TABLE IF NOT EXISTS graphs (
            name VARCHAR(256) NOT NULL PRIMARY KEY
       );
       """
        self.__cursor.execute(statement1)
        
        # delete temporary graphs of previous sessions
        for graph_name in self.get_graphs():
            if graph_name.startswith(self.__temp_prefix):
                self.drop_graph(graph_name)


    def __contains__(self, name):
        name = self.__table(name)
        try:
            self.create_graph(name)
            self.drop_graph(name)
            return False
        except:
            return True

    def create_graph(self, name):
        name = self.__table(name)
        self.__cursor.execute("INSERT INTO graphs VALUES ('%s')" % name)

        statement1= """        
        CREATE TABLE %s_nodes (
            node VARCHAR(256) NOT NULL PRIMARY KEY,
            count BIGINT NULL                             
            
       );
       """
        self.__cursor.execute(statement1 % (name))
        
        statement1bis= """        
        CREATE TABLE %s_nodes_attrs (
            node VARCHAR(256) NOT NULL,
            type VARCHAR(256) NOT NULL,
            attr VARCHAR(256) NOT NULL,
            count INT NOT NULL
       );
       """
        self.__cursor.execute(statement1bis % (name))
        
        statement2 = """
        CREATE TABLE %s_edges (
            node VARCHAR(256) NOT NULL,                  
            neighbor VARCHAR(256) NOT NULL            
       );
       """
        self.__cursor.execute(statement2 % (name))
        
        statement2bis= """        
        CREATE TABLE %s_edges_attrs (
            node VARCHAR(256) NOT NULL,                  
            neighbor VARCHAR(256) NOT NULL,
            type VARCHAR(220) NOT NULL,
            attr VARCHAR(256) NOT NULL,
            count INT NOT NULL
       );
       """
        self.__cursor.execute(statement2bis % (name))
        
        statement4 = """
        CREATE INDEX %s_edges_index
        ON %s_edges (node)
       """
        self.__cursor.execute(statement4 % (name,name))
       
        statement4bis = """
        CREATE INDEX %s_edges_attrs_index
        ON %s_edges_attrs (node, type, attr)
       """
        self.__cursor.execute(statement4bis % (name,name))
       
        statement4tris = """
        CREATE INDEX %s_nodes_attrs_index
        ON %s_nodes_attrs (node, type, attr)
       """
        self.__cursor.execute(statement4tris % (name,name))
       
        statement4quatris = """
        CREATE INDEX %s_nodes_attrs_index2
        ON %s_nodes_attrs (node)
       """
        self.__cursor.execute(statement4quatris % (name,name))
       
        statement5 = """
        CREATE UNIQUE INDEX %s_edges_index2
        ON %s_edges (node, neighbor)
       """
        self.__cursor.execute(statement5 % (name,name))

        statement5bis = """
        CREATE INDEX %s_edges_attrs_index2
        ON %s_edges_attrs (node, neighbor, type, attr)
       """
        self.__cursor.execute(statement5bis % (name,name))

       
#        statement6 = """
#        CREATE UNIQUE INDEX %s_edges_index3
#        ON %s_edges (neighbor)
#       """
#        self.__cursor.execute(statement6 % (name,name))
       
    def drop_graph(self, name):
        name = self.__table(name)        
        self.__cursor.execute("DELETE FROM graphs WHERE name='%s'" % name)

        drop_statement1= """        
        DROP TABLE %s_nodes;
       """
        self.__cursor.execute(drop_statement1 % (name))
        
        drop_statement1bis= """        
        DROP TABLE %s_nodes_attrs;
       """
        self.__cursor.execute(drop_statement1bis % (name))
        
        drop_statement2 = """
        DROP TABLE %s_edges;
       """
        self.__cursor.execute(drop_statement2 % (name))
        
        drop_statement2bis = """
        DROP TABLE %s_edges_attrs;
       """
        self.__cursor.execute(drop_statement2bis % (name))
        
    def __get_something(self, table, node=None):
        table = self.__table(table)
        cursor = self.__cursor
        if not node:
            cursor.execute("SELECT * FROM %s" % table)
            return cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM %s WHERE node='%s'" % (table,node))
            return cursor.fetchall()            
        
    def get_graphs(self, include_temp=True):
        for row in self.__get_something('graphs'):
            if include_temp or not row[0].startswith(self.__temp_prefix):                 
                yield row[0]
        
    def get_nodes(self, graph_name, node=None):
        for row in self.__get_something('%s_nodes' % graph_name, node):
            yield row[0]

    def get_nodes_attrs(self, graph_name, node=None, type=None):
        if not type:
            for row in self.__get_something('%s_nodes_attrs' % graph_name, node):
                yield row
        else:
            for row in self.__get_something_type('%s_nodes_attrs' % graph_name, node, type):
                yield row
            
    def __get_something_type(self, table, node=None, type=None):            
        table = self.__table(table)
        cursor = self.__cursor
        if not node:
            cursor.execute("SELECT * FROM %s WHERE type='%s'" % (table,type))
            return cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM %s WHERE node='%s' AND type='%s'" % (table,node,type))
            return cursor.fetchall()            

    def get_edges(self, graph_name, node=None):
        for row in self.__get_something('%s_edges' % graph_name, node):
            yield row
 
    def get_edges_attrs(self, graph_name, n1=None):
        for row in self.__get_something('%s_edges_attrs' % graph_name, n1):
            yield row
 
    def get_edge(self, graph_name, node1, node2):
        graph_name = self.__table(graph_name)
#        if node2 < node1:
#            node1, node2 = node2, node1
        self.__cursor.execute("SELECT * FROM %s_edges WHERE node='%s' AND neighbor='%s'" % (graph_name,node1,node2))
        return self.__cursor.fetchall()            

    def get_edge_attrs(self, graph_name, node1, node2=None):
        graph_name = self.__table(graph_name)
        if node2:
            self.__cursor.execute("SELECT * FROM %s_edges_attrs WHERE node='%s' AND neighbor='%s'" % (graph_name,node1,node2))
        else:
            self.__cursor.execute("SELECT * FROM %s_edges_attrs WHERE node='%s'" % (graph_name,node1))
        return self.__cursor.fetchall()            

    def exists_node(self, graph_name, node):
        graph_name = self.__table(graph_name)
        for node in self.get_nodes(graph_name, node):
            return True
        for some_node, type, value, count in self.get_nodes_attrs(graph_name, None, Attributes.ALIAS_ATTR):
            if value == node:
                return True
        return False
 
    def exists_node_attr(self, graph_name, node, type, val):
        graph_name = self.__table(graph_name)
        for some_node, type, value, count in self.get_nodes_attrs(graph_name, node, type):
            if value == val:
                return True
        return False
 
    def exists_edge_attr(self, graph_name, node1, node2, type, val):
        graph_name = self.__table(graph_name)
        for node1_bis, node2_bis, type, value, count in self.get_edges_attrs(graph_name, node1):
            if node2_bis == node2 and value == val:
                return True
        return False
 
    def exists_edge(self, graph_name, node1, node2):
        graph_name = self.__table(graph_name)
        for node in self.get_edge(graph_name, node1, node2):
            return True
        return False
 
    def add_node(self, graph_name, node, count=None):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
        if not count:
            count = 'NULL'
        count = str(count)        
        cursor.execute("INSERT INTO %s_nodes VALUES ('%s',%s)" % (graph_name, node, count))
        self.add_node_attr(graph_name, node, Attributes.ALIAS_ATTR, node)

    def add_node_attr(self, graph_name, node, type, value):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
        value = str(value)
        if not self.exists_node_attr(graph_name, node, type, value):
            cursor.execute("INSERT INTO %s_nodes_attrs VALUES ('%s','%s','%s', 1)" % (graph_name, node, type, value))
        else:
            cursor.execute("UPDATE %s_nodes_attrs SET count = count + 1 WHERE node='%s' AND type='%s' AND attr='%s'" % (graph_name, node, type, value))

    def add_edge(self, graph_name, node1, node2):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
#        if node2 < node1:
#            node1, node2 = node2, node1
        cursor.execute("INSERT INTO %s_edges VALUES ('%s','%s')" % (graph_name, node1, node2))
        if not self.exists_node(graph_name, node1):
            self.add_node(graph_name, node1)
        if not self.exists_node(graph_name, node2):
            self.add_node(graph_name, node2)

    def add_edge_attr(self, graph_name, n1, n2, type, value):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
        value = str(value)
        if not self.exists_edge_attr(graph_name, n1, n2, type, value):
            cursor.execute("INSERT INTO %s_edges_attrs VALUES ('%s','%s','%s','%s', 0)" % (graph_name, n1, n2, type, value))
            #cursor.execute("INSERT INTO %s_nodes_attrs VALUES ('%s','%s','%s', 0)" % (graph_name, node, type, value))
        else:
            cursor.execute("UPDATE %s_edges_attrs SET count = count + 1 WHERE node='%s' AND neighbor='%s' AND type='%s' AND attr='%s'" % (graph_name, n1, n2, type, value))

    def delete_node(self, graph_name, node):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
        cursor.execute("DELETE FROM %s_nodes WHERE node='%s'" % (graph_name, node))
        cursor.execute("DELETE FROM %s_edges WHERE node='%s'" % (graph_name, node))
        cursor.execute("DELETE FROM %s_edges WHERE neighbor='%s'" % (graph_name, node))

    def delete_edge(self, graph_name, node1, node2):
        graph_name = self.__table(graph_name)
        cursor = self.__cursor
        cursor.execute("DELETE FROM %s_edges WHERE node='%s' AND neighbor='%s'" % (graph_name, node1, node2))
   
    def get_temporary_graph(self):
        return self.__temp_prefix + base64.b64encode(md5.new(str(time.time())).digest()).replace('/','A').replace('+','A')[:12]
        #return 'temp' #-%f' % time.time()
    
if __name__=='__main__':
    
    p = GraphBuilderRep()
    
    g_name = 'AAA'
    if not p.exists_graph(g_name):
        p.create_graph(g_name)
    p.drop_graph(g_name)
 
    p.create_graph(g_name)
    print p.exists_node(g_name, 'Alice')
    p.add_node(g_name, 'Alice')
    print p.exists_node(g_name, 'Alice')
    
    p.add_edge(g_name, 'Alice', 'Bob')
    p.add_edge(g_name, 'Alice', 'Eve')

    for node in p.get_nodes(g_name):
        print node
    
    for edge in p.get_edges(g_name):
        print edge

    p.drop_graph(g_name)
        
