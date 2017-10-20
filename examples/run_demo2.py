
from run_speakers import speakers
from exomind import *

g = 'blind_graph'

del_graph(g)
graph(g)
focus_graph(g)

for s in speakers:
	node(s)

load_lamb_herd()
add_expander('GraphBot::with_all')
add_weigh_scale('SearchEngineBot::normalized_se_distance', 0.0, 0.5, 'security')
add_weigh_scale('SearchEngineBot::normalized_se_entropy', 0.0, 0.4, 'security')
f('gerardo richarte')
crawl(len(speakers))

plot()
ls()


#save_cache()

