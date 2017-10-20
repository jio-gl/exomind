
import exomind

e = exomind

e.del_graph('graph_neigh')
e.graph('graph_neigh')
e.focus_graph('graph_neigh')
e.node('mattharding2718')
e.f('mattharding2718')

e.load_lamb_herd()

e.add_expander('YouTubeBot::users_from_favorite_videos')
e.crawl(4)


e.f('mattharding2718')
e.clear_expanders()
e.add_expander('GraphBot::neighbors')
e.add_weigh_scale('SearchEngineBot::normalized_se_distance', 0.0, 0.5, '')
e.crawl(4)

#fr(200)
e.plot()


