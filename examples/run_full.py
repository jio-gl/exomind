
from exomind import *

g = 'full_graph'
n = 'john doe'

del_graph(g)
graph(g)
focus_graph(g)
node(n)
focus(n)

load_lamb_herd()
add_expander('SearchEngineBot::name_to_self_emails')
add_expander('SearchEngineBot::name_to_emails')
add_expander('FacebookBot::friends')
add_expander('TwitterBot::following')
add_expander('LinkedInBot::recommendations')
crawl(100)

infiltrate_chat('hi')




