
import random
import re
import time

from html2text import html2text
from distance import NGD
from translator import Translate

from threading import Lock

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

def second_compare(x, y):
    if x[1]>y[1]:
        return 1
    elif x[1]==y[1]:
        return 0
    else: # x<y
        return -1

class ChatBot:
    
    def __init__(self, proxies={}, entropy_filter=True, lang='en', entropy_top=3, query_top=100, fraction = 5):
        self.__ngd = NGD(proxies)
        #self.__ngd.set_context('site:imsdb.com')
        self.__cache = {}
        self.__min_ent = 0.0
        self.__entropy_filter = entropy_filter        
        self.__lang = lang
        self.__entropy_top = entropy_top
        self.__fraction = fraction
        self.__query_top = query_top
        self.__translator = Translate()

        self.__lock = Lock()
        self.__voc_translator = None
        
        random.seed(666)
        
    def set_voc_translator(self, voc_trans=None):
        self.__voc_translator = voc_trans
        
    def entropy_min(self, e_min):
        self.__min_ent = e_min
        
    def reply_to(self, chat_line):
        self.__lock.acquire()
        try:
            chat_line = normalize_token(chat_line)
            if self.__lang != 'en':
                chat_line = self.__translator.translate(chat_line, self.__lang, 'en')
            snippets, answers = [], []             
            while len(answers) == 0:
                snippets = self.__ngd.snippets_query('"%s" site:imsdb.com' % chat_line, self.__query_top)                
                answers = self.__extract_answers(snippets, chat_line)
                if len(answers) == 0:
                    chat_line = chat_line[:-1]
                    if len(chat_line) == 0:
                        break
                    continue

            probabilities = self.__build_probs(answers)
            new_ans = []
            for i in range(min(len(answers),self.__fraction)):
                new_ans.append( self.__choose_random_answer(probabilities) )
            answers = list(set(new_ans))
                    
            new_answers = []
            for ans in answers:
                if self.__entropy_filter:
                    val = self.__ngd.distance(('"%s"' %chat_line, '"%s"' %ans.encode()))
                    if val:
                        print 'search engine distance (choosing response): %s %f' % (ans, val)
                        time.sleep(0.25)
                        new_answers.append((ans,val))                    
            if self.__entropy_filter:
                new_answers.sort(second_compare)
                #new_answers.reverse()
                new_answers = map(lambda x: x[0], new_answers[:self.__entropy_top])
                answers = filter(lambda x: x in new_answers, answers)

            ans = None
            if len(answers) > 0 :
                ans = answers[ random.randint(0,len(answers)-1) ]
            
            if not ans: ans = 'ah';
            
            # use vocabulary translator, if available
            if self.__voc_translator:
                ans = self.__voc_translator(ans)
                
            if ans and self.__lang != 'en':
                ans = self.__translator.translate(ans, 'en', self.__lang).lower()
            if not ans: ans = 'ah'
            return ans
        finally:
            self.__lock.release() # release lock, no matter what        

    
    def __extract_answer(self, snippet, chat_line):
        # [^\.!?]+
        snippet = normalize_token(snippet)        
        snippet = re.sub( '\([^\)]+\) ', '', snippet)
        snippet = re.sub( '\[[^\)]+\] ', '', snippet)
        iterator = re.finditer('[A-Z][A-Z]+ [^\.!?]+[\.!?]', snippet )
        lines = []
        for match in iterator:
            line = match.group()
            #print line
            line_s = line.split(' ')            
            line = ' '.join(line_s[1:]).lower()
            line = html2text(line)
            #print line
            line = line.replace('_', '').replace('\n', '')
            #line = re.sub( '\([^\)]+\) ', '', line)  
            if not '-' in line and not ':' in line and not '**' in line and not '(' in line and not ')' in line and not '"' in line:
                if len(line) > 0 and line[-1] == '.':
                    line = line[:-1]                
                lines.append(line)
            #ret.append(strip(match))
            #print strip(match)
        if len(lines) == 0:
            return ''
        prev = lines[0].lower()
        ret = []
        for i in range(1,len(lines)):
            if chat_line.lower() in prev:
                ret.append(lines[i].lower())
            prev = lines[i].lower()
        return ret
    
    def __extract_answers(self, snippets, chat_line):
        ret, ret_titles = [], []
        for snippet in snippets:
            anss = self.__extract_answer(snippet, chat_line)
            for ans in anss:
                if ans != '':
                    ret.append(ans.strip())
        return ret
    
    def __build_probs(self, answers):
        d = {}
        for ans in answers:
            if not ans in d:
                d[ans] = 1
            else:
                d[ans] += 1
        ret = []
        for ans, cnt in d.iteritems():
            ret.append((ans,float(cnt)/len(answers)))
        return ret
    
    def __choose_random_answer(self, probs):
        rand_float = random.random()        
        sum = 0.0
        ret = None
        for ans, prob in probs:
            sum += prob
            if sum >= rand_float:
                ret = ans
                break
        return ret
    
    def start(self):
        msg = ''
        while msg!='bye':
            msg = raw_input('You: ')            
            ans, title = self.reply_to(msg.strip())
        print 'end of chat.'
    
    def save_cache(self):
        self.__ngd.save_cache()
    
if __name__ == '__main__':
    
    proxies = {}
    bot = ChatBot(proxies)
    #print bot.reply_to('how old are you?')
    bot.start()
