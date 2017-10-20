

class FloatBag:
    
    def __init__(self, bag=None):
        self.__m = {}
        self.__total = 0.0
        if bag:
            self.__total = 1.0
            for word, freq in bag.get_map().iteritems():
                self.__m[word] = float(freq) / len(bag)

    def add(self, item, freq=1.0):
        if not item in self.__m:
            self.__m[item] = freq
        else:
            self.__m[item] += freq
        self.__total += freq
            
    def as_set(self):
        return self.__m.keys()
    
    def size(self):
        ret = 0.0
        for word, freq in self.__m.iteritems():
            ret += freq
        return ret

    def intersection(self, bag):
        i_bag = FloatBag()
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

