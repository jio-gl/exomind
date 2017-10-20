
from FloatBag import FloatBag
from Bag import Bag
from stop_words import all_stop_words

import re, pickle, random
from itertools import groupby
import os.path

random.seed(666)

thesaurus_word_types = [
				'adj.', # adjective
			    'v.',   # verb
			    'n.',   # noun
			    'adv.'  # adverb			    
			    'prep.' # preposition
			    ]


class Dino:

	__debug = True
	
	stop_words = all_stop_words	
				   

	def __init__(self, build_map=False, syn_filter=None):
		
		home_path = os.path.expanduser('~')
		if build_map:
			m = Dino.build_map(syn_filter)
			try:
				output = open('.exomind/syn_map.pickle', 'wb')
			except:
				output = open(home_path + '/.exomind/syn_map.pickle', 'wb')
			pickle.dump(m, output)
		else:
			try:
				pkl_file = open('.exomind/syn_map.pickle', 'rb')			
			except:
				pkl_file = open(home_path + '/.exomind/syn_map.pickle', 'rb')
			m = pickle.load(pkl_file)
		self.__syn_map = m
		self.__fps = {}


	def find_all(w_cont, type='adj.'):
	
		if not type in w_cont:
			return []
	
		syns = []
	
		w_cont_s = w_cont.split('\r\n\r\n')
		good_chunk = ''
		for chunk in w_cont_s:
			if type in chunk.strip():
				good_chunk = chunk.strip()
		
		# si hay ambiguedad, no me interesa
		if len(w_cont_s) > 1:
			return []
		
		good_chunk = good_chunk.replace('\r\n             ','')
		p = re.compile('[0-9]+ [a-z\- ,;]+:')
		# ojo que aca estoy uniendo todos los sentidos!!!
		# TODO: analizar si lo mejor es quedarse solo con el primero.
		possibles_syns = p.findall(good_chunk)
		for possible_syns in possibles_syns:
			possible_syns = possible_syns.replace(':','').replace(';',',')
			possible_syns = ' '.join(possible_syns.split(' ')[1:])
			new_syns = possible_syns.split(', ')
			new_syns = filter(lambda x:len(x)>0, map(lambda x:x.strip(), new_syns))
			# delete synonims like "cast off or aside".
			new_syns = filter(lambda x: not ' or ' in x, new_syns)
			if type == 'adj.':
				new_syns = filter(lambda x: not x.endswith('ed'), new_syns)
			syns += new_syns		
		return syns
	find_all = staticmethod(find_all)
	
	def longest_syn_filter(syn_list):		
		max_len = max(map(len, syn_list))
		ret = []
		for syn in syn_list:
			if len(syn) == max_len:
				ret.append(syn)
		return ret
	longest_syn_filter = staticmethod(longest_syn_filter)	
	
	def shortest_syn_filter(syn_list):		
		min_len = min(map(len, syn_list))
		ret = []
		for syn in syn_list:
			if len(syn) == min_len:
				ret.append(syn)
		return ret
	shortest_syn_filter = staticmethod(shortest_syn_filter)	
	
	def build_map(syn_filter=None, reverse_syns=True):
	
		syn_map = {}
	
		home_path = os.path.expanduser('~')
		try:
			f = open('.exomind/ts.txt')
		except:	
			f = open(home_path + '/.exomind/ts.txt')	
		c = f.read()
		c = c.replace('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-','')
		c = c.replace('...','')
		# special word labels, non-important here.
		c = c.replace('Formal ','')
		c = c.replace('Scots ','')
		c = c.replace('Colloq ','')
		c = c.replace('Slang ','')
		c = c.replace('Taboo ','')
		c = c.replace('Archaic ','')
		c = c.replace('Old-fashioned ','')
		c = c.replace('Technical ','')
		c = c.replace('Literary ','')
		c = c.replace('Brit ','')
		c = c.replace('US ','')
		c = c.replace('Australian ','')
		c = c.replace('Canadian ','')
		c = c.replace('New Zealand ','')
		p = re.compile('[0-9]+\.[0-9]+ [a-zA-Z]+')
		titles = p.findall(c)
		for title in titles:
			c = c.replace(title,'')
		
		s = c.split('\r\n\r\n    ')
	
		w2 = []
		chunk = ''
		for w in s:
			word = w.split(' ')[0].strip()
			if word != '':
				if chunk != '':
					w2.append(chunk.strip())
					chunk = ''
			chunk += '\r\n\r\n' + w	
		if chunk != '':
			w2.append(chunk.strip())
	
		words = []
		#adjs = set([])
		for w in w2:
			word = w.split(' ')[0].strip()
			if word == '':
				 continue
			words.append(word)
			syns = []
			word_types = []
			for thesaurus_word_type in thesaurus_word_types:
				l = len(syns)
				syns += Dino.find_all(w, thesaurus_word_type)
				if l != len(syns):
					word_types.append(thesaurus_word_type)
					
			if len(syns) > 0:
				syns = list(set(syns))
				#adjs.add(word)	
				if syn_filter:			
					syn_map[word] = syn_filter([word] + syns)
				else:
					syn_map[word] = [word] + syns
				if reverse_syns:
					if syn_filter != Dino.shortest_syn_filter and (not 'n.' in word_types and not 'adv.' in word_types and not 'prep.' in word_types):
						for syn in syns:
							if not syn in syn_map:
								syn_map[syn] = ['__' + word]
			
		return syn_map
	build_map = staticmethod(build_map)
		
	
	def extract_words(text):			
		text = text.replace('.','')
		text = text.replace(',','')
		text = text.replace('!','')
		text = text.replace('"','')
		text = text.replace('?','')
		text = text.replace('#','')
		#text = text.lower()
		possible_words = text.split(' ')
		aux = []
		for possible_word in possible_words:
			aux += possible_word.split('\n')
		possible_words = aux
		words = map(lambda x:x.strip(), possible_words)
		words = filter(lambda x:x.lower() == x, words)
		words = filter(lambda x:len(x) > 0, words)
		return words
	extract_words = staticmethod(extract_words)
				
	def create_fingerprint(self, text):	
		words = Dino.extract_words(text)
		good_words = []
		for word in words:
			if word in self.__syn_map:
				good_words.append(word)
		freq_pairs = [(k, len(list(g))) for k, g in groupby(sorted(good_words))]
		bag = Bag(freq_pairs)
		return bag
		
	# create fingerprint from file
	def create_fingerprint_from_file(self, filepath):
		f = open(filepath)
		cont = f.read()
		f.close()
		return self.create_fingerprint(cont)

	def save_fingerprint(fp, filepath):
		fp.save(filepath)
		#output = open(filepath, 'wb')
		#pickle.dump(fp, output)
	save_fingerprint = staticmethod(save_fingerprint)

	def load_fingerprint(filepath):
		fp = Bag()
		fp.load(filepath)
		return fp
		#pkl_file = open(filepath, 'rb')
		#return pickle.load(pkl_file)		
	load_fingerprint = staticmethod(load_fingerprint)

	def fingerprint_dist(fp1, fp2):
		f_fp1 = FloatBag(fp1)
		f_fp2 = FloatBag(fp2)
		return 1.0 - f_fp1.intersection(f_fp2).size()
#		u_fp = fp1.union(fp2)
#		i_fp = fp1.intersection(fp2)
#		return 1.0 - (float(len(i_fp))*2) / len(u_fp) 
	fingerprint_dist = staticmethod(fingerprint_dist)
	
	def fingerprint_dist2(fp1, fp2):
#		f_fp1 = FloatBag(fp1)
#		f_fp2 = FloatBag(fp2)
#		return 1.0 - f_fp1.intersection(f_fp2).size()
		u_fp = fp1.union(fp2)
		i_fp = fp1.intersection(fp2)
		return 1.0 - (float(len(i_fp))*2) / len(u_fp) 
	fingerprint_dist2 = staticmethod(fingerprint_dist2)
	
	def load_fingerprint_db(self, filepath):
		self.__fps[filepath] = Dino.load_fingerprint(filepath)

	def cmp_snd(a, b):
		a, b = a[1], b[1]
		if a < b:
			return 1
		elif b < a:
			return -1
		else:
			return 0
	cmp_snd = staticmethod(cmp_snd)

	def best_match(self, filepath, dist='2'):
		fp = self.create_fingerprint_from_file(filepath)
		dists = []
		for fp_db_filepath, fp_db in self.__fps.iteritems():
			if dist == '1':
				dists.append((fp_db_filepath, Dino.fingerprint_dist(fp, fp_db)))
			else:
				dists.append((fp_db_filepath, Dino.fingerprint_dist2(fp, fp_db)))
		dists.sort(Dino.cmp_snd)
		dists.reverse()
		if len(dists) == 0:
			raise Exception('no fingerprints loaded to database.')
		return dists[0][0] 

	def __build_translator_map(self, text, dst_fp):
		src_fp = self.create_fingerprint(text)
		fp_m = src_fp.get_map()
		fp_total = len(fp_m)
		text_m = {}
		for word, freq in fp_m.iteritems(): # use source text fingerprint as source of translation.
				
			if not self.__syn_map[word][0].startswith('__'):
			#if len(self.__syn_map[word]) > 1: # word defined in thesaurus
				s = self.__syn_map[word]
			else: # word used as synonym in thesaurus, remove '__' at the start of word
				s = self.__syn_map[self.__syn_map[word][0][2:]] + [self.__syn_map[word][0][2:]]
				if word in s:
					s.remove(word)
			aux_s = []
			total_freq_dst = 0
			for syn in s:
				if syn in dst_fp.as_set():
					aux_s.append(syn)
					#print dst_fp.get_map()[syn]
					total_freq_dst += dst_fp.get_map()[syn]
			# use frequency of destinated fingerprint
			s = map(lambda x: (x,float(dst_fp.get_map()[x])/total_freq_dst), aux_s)
			if len(s) > 0: # must contemplate the case where the are no possible replacements.
				text_m[word] = s
		return text_m

	def __probabilistic_repl(self, list_frac):
		rand_float = random.random() # [0.0, 1.0)
		total = 0.0
		for word, frac in list_frac:
			total += frac
			if total > rand_float:
				return word
		raise Exception('list_frac list of pairs (elem,fraction) should have fractions that sum 1.0')
	
	# adapt text to someone's fingerprint
	def translate(self, text, dst_fp):
		trans_map = self.__build_translator_map(text, dst_fp)
		
		tokenized = text.split(' ')
		output = ''
		replacements = 0
		for token in tokenized:
			for src_word in trans_map:
				if (token == src_word 
				    or (src_word+'.') == token
				    or (src_word+',') == token 
				    or (src_word+'!') == token
				    or (src_word+'?') == token
				    or (src_word+'"') == token):
					   replacement = self.__probabilistic_repl(trans_map[src_word])
					   if self.__debug and src_word != replacement:
					   	   print '%s -> %s' % (src_word, replacement)
					   token = token.replace(src_word, replacement)
					   if src_word != replacement:
					   	replacements += 1
					   break
			output += token + ' '
		if len(output) > 0:
			output = output[:-1]
		if self.__debug:
			print 'number of replacements: %d' % replacements
		return output

if __name__ == '__main__':
		
	build_map = True
	
	dino = Dino(build_map)
	
	# from conan doyle's baskervilles and scarlet
	dst_fp = dino.create_fingerprint_from_file('dst.txt')
	text = open('src.txt').read()
	print dino.translate(text, dst_fp)


#Dino.save_fingerprint(fp, 'conan_doyle.fp')
#conan_fp = Dino.load_fingerprint('conan_doyle.fp')
#
## from poe's complete works 1 & 2
#fp2 = dino.create_fingerprint_from_file('poe_vol1.txt')
#Dino.save_fingerprint(fp2, 'poe.fp')
##conan_fp2 = Dino.load_fingerprint('conan_doyle2.fp')
#
## from darwin's letterr 1 & 2
#fp3 = dino.create_fingerprint_from_file('darwin_letters1.txt')
#Dino.save_fingerprint(fp3, 'darwin.fp')
##darwin_fp = Dino.load_fingerprint('darwin.fp')
#
#
##print Dino.fingerprint_dist(conan_fp, conan_fp) 
##print Dino.fingerprint_dist(conan_fp2, conan_fp2)
##print Dino.fingerprint_dist(conan_fp, conan_fp2)
##print Dino.fingerprint_dist(darwin_fp, conan_fp)
##print Dino.fingerprint_dist(darwin_fp, conan_fp2)
#
#dino.load_fingerprint_db('conan_doyle.fp')
#dino.load_fingerprint_db('poe.fp')
#dino.load_fingerprint_db('darwin.fp')
#
#
#file = 'species_darwin.txt'
#print '%s was written by %s' % (file,dino.best_match(file))
#file = 'poe_vol2.txt'
#print '%s was written by %s' % (file,dino.best_match(file))
#file = 'conan-doyle_scarlet.txt'
#print '%s was written by %s' % (file,dino.best_match(file))
