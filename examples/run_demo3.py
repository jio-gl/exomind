
from exomind.LambHerd.Bots.ChatBot import ChatBot
from exomind.LambHerd.Bots.Dino import Dino
from exomind.Exomind import Exomind
from exomind.Attributes import Attributes
import time, sys

proxies = {}
bot = ChatBot(proxies)
dir(bot)

dino = Dino()

em = Exomind()
try:
	em.drop_graph('chat_graph')
except:
	pass
em.create_graph('chat_graph')
em.set_focus_graph('chat_graph')
em.load_lamb_herd()
em.add_expander('SearchEngineBot::vocabulary')
n = 'ivan arce'
em.add_node(n)
em.set_focus_node(n)

def tag_text(node):
	text = ''
	for node, type, attr, count in em.node_attrs(node):
		if type == Attributes.TAG_ATTR:
			text += ' ' + attr
	return text

em.crawl(1)
text = tag_text(n)
ivan_profile = dino.create_fingerprint(text)
ivan_trans = lambda text : dino.translate(text,ivan_profile)


#line = first
for i in range(1000):
	if i % 2 == 0:
		print '----------------------------------'
		sys.stdout.write('You: ')
		line = raw_input()
		print '----------------------------------'
	else:
		line = bot.reply_to(line)
		line = ivan_trans(line)
		print '----------------------------------'
		print 'ivan: ' + line
		print '----------------------------------'
				

#save_cache()


