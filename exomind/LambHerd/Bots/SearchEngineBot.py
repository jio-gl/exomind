
from Harvester import Harvester
from EmailHarvestingCommand import EmailHarvestingCommand
from exomind.Attributes import Attributes
from distance import NGD
from SandMan import SandMan
from Dino import Dino
from exomind.Utils import asciify_snippet, normalize_token
from html2text import html2text

from mechanize import Browser
import urllib
import re

class SearchEngineBot:
    
    def __init__(self):
        pass
        
    def initialize(self, proxies_per_proto={}, user=None, passw=None, debug=False):

        print 'INIT: SearchEngineBot'
        
        self.__br = Browser()
        self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(debug)
        self.__ngd = NGD(proxies_per_proto)
        self.__harvest_command = EmailHarvestingCommand()
        self.__harvest_command.set_only_complete_names(False)
        
        self.__sandman = SandMan('SearchEngineBot')

        # no sign in
        
    def set_proxies_per_proto(self, proxies):
        self.__proxies = proxies
        try:
            self.__ngd.set_proxies(proxies)
        except:
            print 'EXCEPTION on SeachEngineBot, possibly bad user/password or https login don\' work behind a proxy.'
            
        if len(proxies) == 0:
            proxy = None
        else:
            proxy = tuple(proxies['http'].split(':'))
            proxy = (proxy[0], int(proxy[1]))
        self.__proxy = proxy        
        
    def set_sleep_secs(self, secs):
        self.__sandman.set_sleep_secs(secs)        

    def set_sleep_module(self, iterations):
        self.__sandman.set_sleep_module(iterations)        

    def set_sleep_failure(self, secs):
        self.__sandman.set_sleep_failure(secs)

    def set_sleep_random_flag(self, bool):
        self.__sandman.set_sleep_random_flag(bool)

    def self_email(self, email, name):
        if name.lower().startswith(email.split('@')[0].lower()):
            return True
        if len(name.split(' ')) == 1 and name.lower()==email.split('@')[0].lower():
            return True 
        if len(name.split(' ')) == 2 and '.'.join(name.split(' ')).lower()==email.split('@')[0].lower():
            return True
        if len(name.split(' ')) == 2 and '_'.join(name.split(' ')).lower()==email.split('@')[0].lower():
            return True
        if len(name.split(' ')) == 2 and name.split(' ')[0].lower()==email.split('@')[0].lower():
            return True
        if len(name.split(' ')) == 2 and (name.split(' ')[0][0]+name.split(' ')[1]).lower()==email.split('@')[0].lower():
            return True
        return False
        
    def name_to_emails(self, (aliases, graph)):
        self.__harvest_command.set_only_complete_names(False)
        return self.__name_to_emails(aliases, 'all_mails')        
        
    def name_to_self_emails(self, (aliases, graph)):
        self.__harvest_command.set_only_complete_names(False)
        return self.__name_to_emails(aliases, 'self_mails')        
        
    def name_to_emails_strong(self, (aliases, graph)):
        self.__harvest_command.set_only_complete_names(True)
        return self.__name_to_emails(aliases, 'all_mails')        

    def domain_to_emails_strong(self, (aliases, graph)):
        self.__harvest_command.set_only_complete_names(True)
        self.__harvest_command.set_grab_type('domain2name&email')
        email_list = []
        self_attrs, node_dict, link_dict = [], {}, {}
        for alias in aliases:
            self.__sandman.try_to_sleep()
            harvester = Harvester(self.__ngd, self.__harvest_command)            
            email_list += harvester.grab(alias)        
            email_list = self.fix_pair_list(email_list)
            self_attrs, node_dict, link_dict = self.add_email_pair_list(alias, email_list, self_attrs, node_dict, link_dict, 'bla')
        for neigh in link_dict:
            link_dict[neigh] = list(set(link_dict[neigh]))
            node_dict[neigh] = list(set(node_dict[neigh]))
        return self_attrs, node_dict, link_dict        

    def domain_to_emails(self, (aliases, graph)):
        self.__harvest_command.set_only_complete_names(False)
        self.__harvest_command.set_grab_type('domain2name&email')
        email_list = []
        self_attrs, node_dict, link_dict = [], {}, {}
        for alias in aliases:
            self.__sandman.try_to_sleep()
            harvester = Harvester(self.__ngd, self.__harvest_command)            
            email_list += harvester.grab(alias)        
            email_list = self.fix_pair_list(email_list)
            self_attrs, node_dict, link_dict = self.add_email_pair_list(alias, email_list, self_attrs, node_dict, link_dict, 'bla')
        for neigh in link_dict:
            link_dict[neigh] = list(set(link_dict[neigh]))
            node_dict[neigh] = list(set(node_dict[neigh]))
        return self_attrs, node_dict, link_dict        

    def fix_pair_list(self, pair_list):
        final_pair_list = []
        partial_emails = []
        for email, complete_name in pair_list:
            if complete_name != '' and complete_name.strip().split(' ') > 1 and not email in partial_emails:
                complete_name = complete_name.replace('.','')
                final_pair_list.append((email, complete_name))
                partial_emails.append(email)
        return final_pair_list

    def __name_to_emails(self, aliases, mode='all_mails'):
        email_list = []
        self_attrs, node_dict, link_dict = [], {}, {}
        for alias in aliases:
            name = alias
            if not '@' in alias and len(alias.split(' '))==2:
                if mode == 'all_mails':
                    self.__harvest_command.set_grab_type('name2anyemail&domain')
                else:
                    self.__harvest_command.set_grab_type('name2email&domain')
            elif '@' in alias:
                if mode == 'all_mails':                    
                    self.__harvest_command.set_grab_type('email2anyname&email')                    
                else:
                    alias = alias.split('@')[0]
                    self.__harvest_command.set_grab_type('email2name&email')
            else:
                return self_attrs, node_dict, link_dict

            self.__sandman.try_to_sleep()
            harvester = Harvester(self.__ngd, self.__harvest_command)            
            email_list += harvester.grab(alias)
        
            email_list = self.fix_pair_list(email_list)
            self_attrs, node_dict, link_dict = self.add_email_pair_list(name, email_list, self_attrs, node_dict, link_dict, mode)

        for neigh in link_dict:
            link_dict[neigh] = list(set(link_dict[neigh]))
            node_dict[neigh] = list(set(node_dict[neigh]))
        #print str((self_attrs, node_dict, link_dict))
        return self_attrs, node_dict, link_dict        
        
    def add_email_pair_list(self, name, email_list, self_attrs, node_dict, link_dict, mode ):
        for email, complete_name in email_list:
            #print str((email, complete_name))
            if (not complete_name or complete_name == '') and mode != 'self_mails':
                email, complete_name = self.__reconstitute_name(email)
            if self.self_email(email, name):
                self_attrs += [(Attributes.SEARCHENGINEBOT_ALIAS_ATTR,email)]
                self_attrs += [(Attributes.ALIAS_ATTR,email)]
                self_attrs += [(Attributes.EMAIL_ATTR,email)]
                if name != complete_name and complete_name != '':
                    self_attrs += [(Attributes.SEARCHENGINEBOT_ALIAS_ATTR,complete_name)]
                    self_attrs += [(Attributes.ALIAS_ATTR,complete_name)]                    
            elif email != name and complete_name != name: 
                if complete_name == '':
                    if not email in link_dict:
                        link_dict[email] = []
                    if not email in node_dict:
                        node_dict[email] = []                                        
                    node_dict[email] += [(Attributes.SEARCHENGINEBOT_ALIAS_ATTR,email)]
                    node_dict[email] += [(Attributes.ALIAS_ATTR,email)]
                    node_dict[email] += [(Attributes.EMAIL_ATTR,email)]
                else:
                    if not complete_name in link_dict:
                        link_dict[complete_name] = []
                    if not complete_name in node_dict:
                        node_dict[complete_name] = []                                        
                    node_dict[complete_name] += [(Attributes.SEARCHENGINEBOT_ALIAS_ATTR,complete_name)]
                    node_dict[complete_name] += [(Attributes.ALIAS_ATTR,complete_name)]
                    node_dict[complete_name] += [(Attributes.SEARCHENGINEBOT_ALIAS_ATTR,email)]
                    node_dict[complete_name] += [(Attributes.ALIAS_ATTR,email)]
                    node_dict[complete_name] += [(Attributes.EMAIL_ATTR,email)]                    
        return self_attrs, node_dict, link_dict
        
    def __reconstitute_name(self, email):
        id = email.split('@')[0]
        if '.' in id and len(id.split('.')) == 2:
            name, surname = tuple(id.split('.'))
        elif '_' in id  and len(id.split('_')) == 2:
            name, surname = tuple(id.split('_'))
        else:
            return email, ''
        return email, name + ' ' + surname 
        
    def query(self, q):
        self.__sandman.try_to_sleep()
        return self.__ngd.query(q)
    
    def set_context(self, context):
        self.__ngd.set_context(context)
        
    def normalized_se_distance_no_filter(self, (x,y), context=None):
        self.__sandman.try_to_sleep()
        return self.__ngd.distance((x,y), context)
    
    def jaccard_distance_no_filter(self, (x,y), context=None):
        self.__sandman.try_to_sleep()
        return self.__ngd.jaccard_distance((x,y), context)
    
    def hits_distance_no_filter(self, (x,y), context=None):
        self.__sandman.try_to_sleep()
        return self.__ngd.hits_distance((x,y), context)

    def distances(self, pairs, context=None, use_threads=True):
        self.__sandman.try_to_sleep()
        return self.__ngd.distances(pairs, context, use_threads)
    
    def __filtered(self, norm_entropy, min_w, max_w):
        return norm_entropy >= min_w and norm_entropy <= max_w 
    
    def __link_weigh_scale_template(self, val, params, node, func, func_name):
        final_self_attrs, final_node_dict, final_link_dict = val
        nodes = final_node_dict.keys()
        for neigh in nodes:
            self.__sandman.try_to_sleep()
            w, filtered = self.__edge_weigh_scale(node, neigh, params['min_weight'], params['max_weight'], params['context'], func)            
            if not filtered:
                print '(SearchEngineBot::%s) dropping link: %s, %s, weight: %.3f min: %.3f max: %.3f context: %s' % (func_name, node, neigh, w, params['min_weight'], params['max_weight'],params['context'])                
                del final_node_dict[neigh]
                if neigh in final_link_dict:
                    del final_link_dict[neigh]
            else:
                if not neigh in final_link_dict:
                    final_link_dict[neigh] = []
                final_link_dict[neigh] += [(Attributes.WEIGHT_ATTR,str(w))]
        return final_self_attrs, final_node_dict, final_link_dict
    
    def normalized_se_distance(self, val, params, node):
        self.__sandman.try_to_sleep()
        return self.__link_weigh_scale_template(val, params, node, self.normalized_se_distance_no_filter, 'normalized_se_distance')

    def jaccard_distance(self, val, params, node):
        self.__sandman.try_to_sleep()
        return self.__link_weigh_scale_template(val, params, node, self.jaccard_distance_no_filter, 'jaccard_distance_filter')
    
    def hits_distance(self, val, params, node):
        self.__sandman.try_to_sleep()
        return self.__link_weigh_scale_template(val, params, node, self.hits_distance_no_filter, 'hits_distance_filter')
    
    def __edge_weigh_scale(self, node_u, node_v, min_w=None, max_w=None, context=None, func=None):
        node_u, node_v = normalize_token(node_u) , normalize_token(node_v)
        dist = func((node_u, node_v), context)
        if not dist: # distance can't be computed, assume infinite distance and filtered
            return 1.0, False
        else:
            return dist, self.__filtered(dist, min_w, max_w)

    def normalized_se_entropy(self, val, params, node=None):
        self.__sandman.try_to_sleep()
        return self.__node_weigh_template(val, params, node, self.__ngd.only_entropy, 'normalized_se_entropy')

    def se_hits(self, val, params, node=None):
        self.__sandman.try_to_sleep()
        return self.__node_weigh_template(val, params, node, self.__ngd.only_results, 'se_hits')
    
    def __node_weigh_template(self, val, params, node, func, func_name):
        final_self_attrs, final_node_dict, final_link_dict = val
        nodes = final_node_dict.keys()
        for neigh in nodes:
            self.__sandman.try_to_sleep()
            w, filtered = self.__node_weigh_scale(neigh, params['min_weight'], params['max_weight'], params['context'], func)
            if not filtered:
                print '(SearchEngineBot::%s) dropping node: %s, weight: %.3f min: %.3f max: %.3f context: %s' % (func_name, neigh, w, params['min_weight'], params['max_weight'], params['context'])
                if neigh in final_node_dict:
                    del final_node_dict[neigh]
                if neigh in final_link_dict:
                    del final_link_dict[neigh]
            else:
                final_node_dict[neigh] += [(Attributes.WEIGHT_ATTR,str(w))]
        return final_self_attrs, final_node_dict, final_link_dict

        # return weight and bool if filtered
    def __node_weigh_scale(self, string, min_w=None, max_w=None, context=None, func=None):
        string = normalize_token(string) 
        w = func(string, context)
        return w, self.__filtered(w, min_w, max_w)

    def is_chatbot(self):
        return False

    def good_word(self, word):
        m = re.match('[a-zA-Z-]+', word)
        if m and m.group() == word:
            return True
        return False 

    def vocabulary(self, (aliases, graph)):
        
        self_attrs, node_dict, link_dict = [], {}, {}
        vocabulary_patterns = [
                               'said %s',
                               'posted by %s',
                               '%s wrote'
                               ]
        word_list = []
        for alias in aliases:
            self.__sandman.try_to_sleep()
            for pattern in vocabulary_patterns:
                ss = self.__ngd.snippets_query(pattern % alias)
                for s in ss:
                    s = asciify_snippet(s)
                    new_words = Dino.extract_words(s)
                    new_words = map(lambda x: normalize_token(x).encode(), new_words)
                    new_words = filter(self.good_word, new_words)
                    new_words = filter(lambda x: not x in Dino.stop_words, new_words)
                    word_list += new_words
        for word in word_list:
            self_attrs += [(Attributes.TAG_ATTR,str(word.encode()))]
        return self_attrs, node_dict, link_dict

    def save_cache(self):
        self.__ngd.save_cache()
        
if __name__ == '__main__':
    ic = SearchEngineBot()
    ic.initialize({})
