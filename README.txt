What is Exomind?
^^^^^^^^^^^^^^^^

Exomind is an experimental Python console and programmatic framework for building decorated graphs and developing open-source intelligence modules and ideas, centered on social network services, search engines and instant messaging.

jose@mot:~/workspace3/Exomind/examples$ python
>>> from exomind import *
>>> 
>>> n = 'john doe'
>>> node(n)
>>> focus(n)
>>> 
>>> load_lamb_herd()
>>> add_expander('SearchEngineBot::name_to_self_emails')
>>> add_expander('SearchEngineBot::vocabulary')
>>> add_expander('SearchEngineBot::name_to_emails')
>>> add_expander('FacebookBot::friends')
>>> add_expander('TwitterBot::following')
>>> add_expander('LinkedInBot::recommendations')
>>> add_weigh_scale('SearchEngineBot::normalized_se_entropy', 0.0, 0.5)
>>> add_weigh_scale('SearchEngineBot::normalized_se_distance', 0.0, 0.5)
>>> crawl(100)
>>> 
>>> add_chatbot('MSNBot')
>>> infiltrate_chat('hi')
The tool is available HERE. Check the other examples inside the package!

Known Issues
^^^^^^^^^^^^

plot() with weighted graphs only works with normalized_se_distance (edges) and/or normalized_se_entropy (nodes).
Expanders relaying on unstructured third party web pages changing in time may broke.
The chatbot infiltration is not extensible now, only chatbot MSNBot can be used with command infiltrate_chat(). On the other side, new expanders and weigh scales can be added.
Adding Your Own Bots/Expanders

Bots encapulsulate access logic to a specific information source and each can Bot implements one or several expanders to extract information from that source. For example YahooSearchBot may have Yahoo Search API login logic and expanders to request search results information.

A partial recipe follows for YahooSearchBot:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Create file YahooSearchBot.py on folder $PYTHON_LIB/exomind/LambHerd/Bots/, we assume $PYTHON_LIB=/usr/lib/python2.?/site-packages

* Create class YahooSearchBot on that file.

* Add the Bot to $HOME/.exomind/bots.xml and the new expander/s to $HOME/.exomind/expanders.xml.

* Create mandatory methods such as initialize(), set_proxies_per_proto(), set_sleep_secs(), set_sleep_module(), set_sleep_failure() and set_sleep_random_flag(). View other Bots if you want examples, YouTubeBot has no login and LinkedInBot has login. Method initialize() must include any login activity, password should be stored on $HOME/.exomind/bots.xml.

* Create any expander method your_favorite_name(). This method receives a tuple (names, graph), a list of aliases and the focused graph, and must return a (self_node_attr_list,neighbor_attr_dictionary, link_attr_dictionary) where the keys of the dictionaries are the names of the new neighbors of the node (self_node) expanded. The list are made of pairs (attr_type, attr_value), for example adding tags to links and aliases to neighbors...

        self_attrs, node_dict, link_dict = [], {}, {}
        for neigh, tags in zip(complete_names, tags_videos):
            if neigh != name:
                if not neigh in link_dict:
                    link_dict[neigh] = []
                if not neigh in node_dict:
                    node_dict[neigh] = []
                for tag in tags:
                    link_dict[neigh] += [(Attributes.TAG_ATTR,tag)]
                link_dict[neigh] += [(Attributes.YOUTUBE_ALIAS_ATTR,'')]
                node_dict[neigh] += [(Attributes.YOUTUBE_ALIAS_ATTR,neigh)]
                node_dict[neigh] += [(Attributes.ALIAS_ATTR,neigh)]
        return self_attrs, node_dict, link_dict

* New attribute types can be added at $PYTHON_LIB/exomind/Attributes.py.

* Finally add line from YahooSearchBot import YahooSearchBot to file

$PYTHON_LIB/exomind/LambHerd/Bots/__init__.py

* This step will disappear in future version using metaprogramming (!).

* Add any weigh scale method you want as favorite_weigh_scale_name(). This kind of method receives a tuple (self_node_attr_list,neighbor_attr_dictionary, link_attr_dictionary) to be filtered, a dictionary with parameters possibly including 'min_weight', 'max_weight' and 'context'. Finally this method receives the name of the expanded node. It must returns the same as any expander (self_node_attr_list,neighbor_attr_dictionary, link_attr_dictionary), but with any desired neighbor filtered and weight (or any) attributes added.

* Follow the existing Bot examples!
