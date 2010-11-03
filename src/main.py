from PIL import Image
import numpy, os, shutil

make_anyway = True # don't generate image files if they are present
a = 100; pixel_factor = 6

rule_numbers = range(256)

rule_study_number = 20


import rulestudy
from process import Ca

def out_html(rule_numbers):
    # copy template dirs
    if not os.path.exists("../output/js") or not os.path.exists("../output/css"):
        shutil.copytree("../output_template/js","../output/js/")
        shutil.copytree("../output_template/css","../output/css/")
    
    f = open("../output_template/index.html",'r')
    template = f.read()
    files = []
    for r in rule_numbers:
        bi = Ca().d2b(r)
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
    if not os.path.exists("../output/images"): # output path must exist
        os.makedirs("../output/images")
    
    if make_anyway or not os.path.isfile("../output/images/rule%s.png" % rule_numbers[len(rule_numbers)-1]): # last file exists -> don't generate
        for rn in rule_numbers:
            # init first line
            line = list(numpy.zeros(a, dtype=numpy.int))
            line[a/2] = 1
            
            im = Ca().getImage(line,rn)
        
            im.save("../output/images/t_rule%s.png" % rn, "PNG")
            im = im.resize((a*pixel_factor,a*pixel_factor), Image.NEAREST)
            
            im.save("../output/images/rule%s.png" % rn, "PNG")
            
            print "Rule %s" % rn
            
            rulestudy.foo(rn,"../output/rules/",a,rule_study_number)
            
            print "Study complete"
            
    out_html(rule_numbers)
    rulestudy.html_out("../output/rules/")
    
    
main()