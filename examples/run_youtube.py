import exomind


e = exomind

e.del_graph('bla_graph3')
e.graph('bla_graph3')
e.focus_graph('bla_graph3')
e.node('jcl5m')
e.f('jcl5m')

e.load_lamb_herd()
e.add_expander('YouTubeBot::users_from_favorite_videos')
e.crawl(10)


e.plot()



