
from exomind.Exomind import Exomind
from exomind.algorithm import *

e = Exomind()
try:
	e.create_graph('bla_graph3')
except:
	pass
g = e.get_graph_instance('bla_graph3')

NWB.export_directed_unweighted(g, './bla.nwb')
GraphML.export_directed_unweighted(g, './bla.graphml')
