
from exomind import *
from exomind.Attributes import Attributes


del_graph('chat_graph')
graph('chat_graph')
focus_graph('chat_graph')

node('Alice')

node('Bob')
add_node_attr('Bob', Attributes.LINKEDIN_ALIAS_ATTR, 'bla@youtube.com')
add_node_attr('Bob', Attributes.WEIGHT_ATTR, '0.75')
node('F2')
add_node_attr('F2', Attributes.LINKEDIN_ALIAS_ATTR, 'bla2@youtube.com')
add_node_attr('F2', Attributes.WEIGHT_ATTR, '0.5')
node('F3')
add_node_attr('F3', Attributes.LINKEDIN_ALIAS_ATTR, 'bla3@youtube.com')
link('Alice', 'Bob')
add_link_attr('Alice','Bob', Attributes.WEIGHT_ATTR, '0.25')
#link('Alice', 'F2')
#link('Alice', 'F3')

node('F4')
add_node_attr('F4', Attributes.FACEBOOK_ALIAS_ATTR, 'bla@youtube.com')
add_node_attr('F4', Attributes.WEIGHT_ATTR, '0.75')
node('F5')
add_node_attr('F5', Attributes.FACEBOOK_ALIAS_ATTR, 'bla2@youtube.com')
add_node_attr('F5', Attributes.WEIGHT_ATTR, '0.5')
node('F6')
add_node_attr('F6', Attributes.FACEBOOK_ALIAS_ATTR, 'bla3@youtube.com')
link('Alice', 'F4')
add_link_attr('Alice','F4', Attributes.WEIGHT_ATTR, '0.25')
link('Alice', 'F5')
add_link_attr('Alice','F5', Attributes.WEIGHT_ATTR, '0.4')
#link('Alice', 'F6')
#
node('F7')
add_node_attr('F7', Attributes.TWITTER_ALIAS_ATTR, 'bla@youtube.com')
add_node_attr('F7', Attributes.WEIGHT_ATTR, '0.75')
node('F8')
add_node_attr('F8', Attributes.TWITTER_ALIAS_ATTR, 'bla2@youtube.com')
add_node_attr('F8', Attributes.WEIGHT_ATTR, '0.5')
node('F9')
add_node_attr('F9', Attributes.TWITTER_ALIAS_ATTR, 'bla3@youtube.com')
link('Alice', 'F7')
add_link_attr('Alice','F7', Attributes.WEIGHT_ATTR, '0.25')
#link('Alice', 'F8')
#link('Alice', 'F9')


p()
