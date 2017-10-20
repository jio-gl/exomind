
from exomind import Exomind
from exomind.Attributes import Attributes

em = Exomind()

graph = 'real'

# set the victim
person = 'john doe'

try:
	em.drop_graph(graph)
except:
	pass
em.create_graph(graph)
em.set_focus_graph(graph)


em.add_node(person)

em.load_lamb_herd()
em.add_expander('SearchEngineBot::vocabulary')
em.add_expander('FacebookBot::friends')
em.add_expander('TwitterBot::following')
em.add_expander('TwitterBot::favorites')
em.add_expander('LinkedInBot::recommendations')
em.add_expander('LinkedInBot::also_viewed')
em.add_expander('SearchEngineBot::name_to_emails')
em.add_expander('SearchEngineBot::name_to_self_emails')
em.add_weigh_scale('SearchEngineBot::normalized_se_distance', 0.0, 0.4)
em.add_weigh_scale('SearchEngineBot::normalized_se_entropy', 0.0, 0.4)
em.set_focus_node(person)
em.crawl(1)

em.clear_expanders()
em.add_expander('SearchEngineBot::name_to_self_emails')

neighs = 0
for link in em.edges(person):
	print link
	neighs +=1

print 'TOTAL: %d' % neighs

for link in em.edges(person):
	print link
	neigh = link[1]
	em.set_focus_node(neigh)
	em.crawl(1)


em.set_focus_node(person)
em.add_chatbot('MSNBot')
em.infiltrate_chat('hey', 300)


