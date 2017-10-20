
import re

from html2text import html2text
from exomind.Utils import asciify_snippet


class Harvester:

    def __init__(self, ngd, command=None):
        self.__ngd = ngd
        self.__command = command
    
    def set_command(self, command):
        self.__command = command
    
    def grab(self, node):
        print '(SearchEngineBot) crawling for "%s"' % str(node)
        inputs = self.__command.get_inputs(node)        
        total_matches = []
        for input in inputs:
            regexes = self.__command.get_regexes(input)
            matches = []
            snippets = self.__ngd.snippets_query(input)
            for snippet in snippets:
                snippet = asciify_snippet(snippet)
                #snippet = html2text(snippet).encode()
                for regex in regexes:
                    new_matches = self.__get_matches(snippet, regex)
                    matches += self.__command.purify_matches(new_matches)
            total_matches += matches
        total_matches = list(set(total_matches))
        return total_matches

    def __get_snippets(self):
        return self.__ngd.snippets_query()
    
    def __get_matches(self, snippet, regex):
        compiled_regex = re.compile(regex, re.IGNORECASE)
        return compiled_regex.findall(snippet)
    
    
    
