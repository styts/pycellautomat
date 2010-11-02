from PIL import Image
import numpy, os, shutil

make_anyway = True # don't generate image files if they are present
w = 5 ; h = w
pixel_factor = 10

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
    
    if rule_nr == 14:
        print "LINE:",line
    for i in range(0,len(line)):
        x = line[i:i+3]
        trans = apply_rules(rules,x)
        if rule_nr == 14:
            print "x:", x
            print "trans:", trans
            
        if len(x) > 2: # furthermost right ones are ignored
            next_line.append(trans)
        
    
    return next_line

def bar(line,pix,rule_nr):
    # transform and paint lines
    for i in range(0,h):
        for j in range(0,w):
            c = line[j]
            pix[j,i] = (0,0,0) if c == 1 else (255,255,255)
        #print line
        line = foo(line,rule_nr)

def out_html(rule_numbers):
    # copy template dirs
    if not os.path.exists("../output/js") or not os.path.exists("../output/css"):
        shutil.copytree("../output_template/js","../output/js/")
        shutil.copytree("../output_template/css","../output/css/")
    
    f = open("../output_template/index.html",'r')
    template = f.read()
    files = []
    for r in rule_numbers:
        bi = d2b(r)
        s = """
        <li>
            <a class="thumb" name="rule%s" href="images/rule%s.png" title="Rule %s (%s)">
            <img src="images/t_rule%s.png" alt="Rule %s (%s)" />
            </a>
            <div class="caption">
            Rule %s (%s)
            </div>
        </li>
        """ % (r, r, r, bi, r, r, bi, r, bi)
        files.append(s)
        #if (r%10 == 0): files.append("<br/>") 
    
    files = "\n".join(files)
    template = template % {"files" : files}
    
    fp = open("../output/main.html",'w')
    fp.write(template)
    fp.close()
    print "../output/main.html generated"
    
def main():
    if make_anyway or not os.path.isfile("../output/images/rule%s.png" % rule_numbers[len(rule_numbers)-1]): # last file exists -> don't generate
        for rn in rule_numbers:
            # create image
            im = Image.new("RGB", (w, h), "white")
            pix = im.load() # pixel access matrix
            
            # init first line
            line = list(numpy.zeros(w+2, dtype=numpy.int))
            line[w/2] = 1
            
            bar(line,pix,rn)
        
        
            if not os.path.exists("../output/images"):
                os.makedirs("../output/images")
            
            im.save("../output/images/t_rule%s.png" % rn, "PNG")
            im = im.resize((w*pixel_factor,h*pixel_factor), Image.NEAREST    )
            
            im.save("../output/images/rule%s.png" % rn, "PNG")
            
            print "Rule %s" % rn
        
    out_html(rule_numbers)
    
main()