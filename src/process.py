from numpy import zeros
from PIL import Image

class Ca:
    
    """Returns the binary representation of a decimal integer"""
    def d2b(self,n):
        bi = bin(n)
        bi = bi[2:]
        while len(bi)<8:
            bi = '0' + bi
        return bi
    
    """Rules are the transformations of a 3-tuple of binary neighbours into a output bit. n defines the Wolfram Rule"""
    def _get_rules(self,n):
        bi = self.d2b(n)
        rules = [# [input]      [out]
                 ([1, 1, 1] , int(bi[0])),
                 ([1, 1, 0] , int(bi[1])),
                 ([1, 0, 1] , int(bi[2])),
                 ([1, 0, 0] , int(bi[3])),
                 ([0, 1, 1] , int(bi[4])),
                 ([0, 1, 0] , int(bi[5])),
                 ([0, 0, 1] , int(bi[6])),
                 ([0, 0, 0] , int(bi[7])),
                 ]
        return rules
    
    def _apply_rules(self,rules,x):
        # transform according to rules
        for r in rules:
            if r[0] == x:
                return r[1]
        return x
    
    """Return the transformed nextline. adds leading and trailing zeros for working with"""
    def _foo(self,line,rule_nr):
        line.append(0)
        line.insert(0,0)
    
        next_line = []
        rules = self._get_rules(rule_nr)
        
        for i in range(0,len(line)):
            x = line[i:i+3]
            trans = self._apply_rules(rules,x)
            if len(x) > 2: # furthermost right ones are ignored
                next_line.append(trans)
        return next_line
    
    """returns 2-dimensional array"""
    def doit(self,line,rule_nr):
        a = len(line)
    
        #extend the matrix
        matrix = zeros([a*3,a], int)
        z = list(zeros([a],int))
        line = z + line + z
        
        
        sliced = []
        for i in range(0,a):
            #print line
            for j in range(0,a):
                matrix[j,i] = line[j]
            sliced.append(line[a:a*2])
            line = self._foo(line,rule_nr)
        
        #print "sli:", sliced
        return sliced
    
    """returns a PIL Image. calls doit"""
    def getImage(self,line,rule_nr):
        a = len(line)
        # create image
        im = Image.new("RGB", (a, a), "white")
        pix = im.load() # pixel access matrix
        
        matrix = self.doit(line,rule_nr)
        for i in range(0,a):
            for j in range(0,a):
                v = matrix[i][j]
                pix[j,i] = (0,0,0) if v == 1 else (255,255,255)
        
        return im