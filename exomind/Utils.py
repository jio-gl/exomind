
import re
import sys

def normalize_token(token):
    if token:
        new_token = ''
        for char in token:
            if ord(char) < 128:
                new_token += char
        token = new_token
        token = token.replace('\'', '`')
        return token
    else:
        return token
        
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def to_sql_token(token):
    return re.sub('[^a-zA-Z0-9]', '_', token)

def asciify_snippet(snippet):
    return snippet.replace('<em>','').replace('</em>','').replace('<b>','').replace('</b>','').replace('&lt;','').replace('&gt;','')
