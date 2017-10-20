
from TextTool import TextTool

import re

class RegexTextTool(TextTool):
    
    TOKEN_REGEX = '[a-zA-Z0-9\-_]+'
    
    def __init__(self, text=None):
        TextTool.__init__(self, text)    
    
    def set_prefix(self, prefix):
        self.__prefix = prefix

    def set_suffix(self, suffix):
        self.__suffix = suffix
    
    def set_central_regex(self, central_regex):
        self.__central_regex = central_regex

    def remove_escaping(self, string):
        return string.replace('\?','?').replace('\.','.').replace('\[','[').replace('\]',']').replace('\(','(').replace('\)',')')

    def __strip_element(self, element_match):        
        return element_match[len(self.remove_escaping(self.__prefix)):-len(self.remove_escaping(self.__suffix))]
    
    def extract_elements(self):
        self.__complete_regex = self.__prefix + self.__central_regex + self.__suffix
        elem_matches = re.findall(self.__complete_regex, self.text)
        return map(self.__strip_element, elem_matches)
 