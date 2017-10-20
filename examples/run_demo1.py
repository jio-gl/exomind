
from exomind import *

g = 'mail_graph'
n = 'dragos ruiu'

del_graph(g)
graph(g)
focus_graph(g)
node(n)
focus(n)

load_lamb_herd()
add_expander('SearchEngineBot::name_to_emails')
crawl(1)

plot()

node_attrs(n)

nodes()

focus('mike silbersack')
crawl(5)

node_attrs('mike silbersack')
plot()

#save_cache()
