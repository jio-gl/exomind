
class Bag:
    
    def __init__(self, freq_pairs=None):
        self.__m = {}
        self.__total = 0
        if freq_pairs:
            for item,freq in freq_pairs:
                self.__m[item] = freq
                self.__total += freq

    def get_map(self):
        return self.__m
    
    def add(self, item, freq=1):
        if not item in self.__m:
            self.__m[item] = freq
        else:
            self.__m[item] += freq
        self.__total += freq

    def __len__(self):
        return self.__total
    
    def as_set(self):
        return self.__m.keys()
    
    def intersection(self, bag):
        i_bag = Bag()
        if len(self.as_set()) < len(bag.as_set()):
            m1 = self.__m
            m2 = bag.__m
        else:
            m2 = self.__m
            m1 = bag.__m
        for word in m1:
            if word in m2:
                freq = min(m1[word], m2[word])
                i_bag.add(word,freq)
        return i_bag
                        
    def union(self, bag):
        u_bag = Bag()
        for word, freq in self.__m.iteritems():
            u_bag.add(word, freq)
        for word, freq in bag.__m.iteritems():
            u_bag.add(word, freq)
        return u_bag

    def save(self, filepath):
        f = open(filepath, 'w')
        f.write('%s\n' % self.__total)
        for word, freq in self.__m.iteritems():
            f.write('%s|%d\n' % (word,freq))
        f.close()

    def load(self, filepath):
        self.__total = 0
        self.__m = {}

        f = open(filepath)
        lines = f.readlines()
        f.close
        
        for line in lines[1:]:
            if line.strip() == '':
                continue                        
            word = line.split('|')[0]
            freq = int(line.split('|')[1].strip())
            self.add(word, freq)
