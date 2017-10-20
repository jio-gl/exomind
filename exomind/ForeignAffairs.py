from Attributes import Attributes

import os


class ForeignAffairs:
    
    def __init__(self, exomind):
        
        self.__exomind = exomind
        
    def import_basic(self, filepath):
        
        f = open(os.path.abspath(filepath))
        try:
            for line in f:
                vals = line.strip().split(' ')
                if len(vals) == 2:
                    self.__exomind.add_edge(vals[0].strip(), vals[1].strip())
                elif len(vals) != 1 or (len(vals) == 1 and vals[0] != ''):
                    raise ExomindException('bad basic format in file %s' % filepath)
        finally:
            f.close()        

    def export_tagged(self, filepath):
        
        f = open(os.path.abspath(filepath), 'w')
        try:
            for node, neigh in self.__exomind.edges():
                tags = []
                for n1, n2, type, attr in self.__exomind.edge_attrs(node, neigh):
                    if type == Attributes.TAG_ATTR:
                        tags.append(attr)
                f.write('%s\t\t%s\t\t%s\n' % (node, neigh, '|'.join(tags)))                
        finally:
            f.close()        


if __name__=='__main__':
    fa = ForeignAffairs(None)
    pass