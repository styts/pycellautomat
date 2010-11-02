from PIL import Image
import numpy, os

#rule_nr = 110
w = 200 ; h = w
pixel_factor = 2

rule_numbers = [110]
rule_numbers = range(20)
#rule_numbers = range(256)
    

def d2b(n):
    bi = bin(n)
    bi = bi[2:]
    while len(bi)<8:
        bi = '0' + bi
    return bi

"""Rules are the transformations of a 3-tuple of binary neighbours into a output bit. n defines the Wolfram Rule"""
def get_rules(n):
    bi = d2b(n)
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

def apply_rules(rules,x):
    # transform according to rules
    for r in rules:
        if r[0] == x:
            return r[1]
    return x

"""Return the transformed nextline. adds leading and trailing zeros for working with"""
def foo(line,rule_nr):
    line.append(0)
    line.insert(0,0)

    next_line = []
    
    rules = get_rules(rule_nr)
    for i in range(0,len(line)):
        x = line[i:i+3]
        trans = apply_rules(rules,x)
        if len(x) > 2: # furthermost right ones are ignored
            next_line.append(trans)
    return next_line

def bar(line,pix,rule_nr):
    # transform and paint lines
    for i in range(0,h):
        #print line
        line = foo(line,rule_nr)
        for j in range(0,w):
            c = line[j]
            pix[j,i] = (0,0,0) if c == 1 else (255,255,255)

def out_html(rule_numbers):
    fp = open("../output/main.html",'w')
    s = "<html><body>\n"
    for r in rule_numbers:
        s += "\t<span class='bla'>"
        s += "\t\t<span class='dec'>Rule %s</span>" % r
        s += "\t\t<pre class='bi' >%s</pre>" % d2b(r)
        s += "\t\t<img src='images/rule%s.png'>\n" % r
        s += "\t</span>"
    s += "</body></html>\n"
    fp.write(s)
    fp.close()
    print "output/main.html generated"
    
def main():
    if not os.path.isfile("../output/images/rule%s.png" % rule_numbers[len(rule_numbers)-1]): # last file exists -> don't generate
        for rn in rule_numbers:
            # create image
            im = Image.new("RGB", (w, h), "white")
            pix = im.load() # pixel access matrix
            
            # init first line
            line = list(numpy.zeros(w, dtype=numpy.int))
            line[w/2] = 1
            
            bar(line,pix,rn)
        
            im = im.resize((w*pixel_factor,h*pixel_factor), Image.NEAREST )
            if not os.path.exists("../output/images"):
                os.makedirs("../output/images")
            im.save("../output/images/rule%s.png" % rn, "PNG")
            
            print "Rule %s" % rn
        
    out_html(rule_numbers)
    
main()