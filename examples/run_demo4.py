
# WARNING: this demo script will add your MSN user ID (if you have set one)
# 	   to a contact list of the author, actually two lists.

print 'WARNING: this demo script will add your MSN user ID (if you have set one)'
print '         to a contact list of the author, actually two lists'

from exomind import *
from exomind.Attributes import Attributes

del_graph('chat_graph')
graph('chat_graph')
focus_graph('chat_graph')

node('termobot')
add_node_attr('termobot', Attributes.EMAIL_ATTR, 'termobot@live.com.ar')
node('termobot2')
add_node_attr('termobot2', Attributes.EMAIL_ATTR, 'termobot2@live.com.ar')

node('ivan arce')
link('ivan arce', 'termobot')
link('ivan arce', 'termobot2')

focus_node('ivan arce')
load_lamb_herd()
add_expander('SearchEngineBot::vocabulary')
crawl(1)

add_chatbot('MSNBot')
infiltrate_chat('hey', 300)


