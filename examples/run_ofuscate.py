import exomind


e = exomind

e.del_graph('ofusc')
e.graph('ofusc')
e.focus_graph('ofusc')
e.node('mattharding2718')
e.f('mattharding2718')

e.add_expander('YouTubeBot::users_from_favorite_videos')
e.add_weigh_scale('GraphBot::ofuscate')
e.crawl(3)

e.plot()



