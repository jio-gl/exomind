import exomind

#exomind.plot()

e = exomind

n = 'dragos ruiu'

#e.context('computer')

e.del_graph('mail_graph')
e.graph('mail_graph')
e.focus_graph('mail_graph')
e.node(n)
e.f(n)

e.load_lamb_herd()
e.add_expander('SearchEngineBot::name_to_emails')

e.add_weigh_scale('SearchEngineBot::normalized_se_distance', 0.0, 0.3, 'security')

e.crawl(1)

e.plot()
#e.save_cache()
