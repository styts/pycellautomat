from process import Ca
import os, random, re
import fnmatch
from PIL import Image

def naturallysorted(L, reverse=False): # helper from http://peternixon.net/news/2009/07/28/natural-text-sorting-in-python/
    """Similar functionality to sorted() except it does a natural text sort
    which is what humans expect when they see a filename list."""
    convert = lambda text: ("", int(text)) if text.isdigit() else (text, 0)
    alphanum = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(L, key=alphanum, reverse=reverse) 

def html_out(outdir):
    
    strings = []
    
    # find all the image files
    dirs = []
    for root, dirnames, filenames in os.walk(outdir):
        for name in dirnames:
            dirs.append(name)
    
    dirs = naturallysorted(dirs)
    for d in dirs:
        #print "d:",d
        files = []
        for root, dirnames, filenames in os.walk(os.path.join(outdir, d)):
              for filename in fnmatch.filter(filenames, 'random_*.png'):
                  files.append(filename)
        files = naturallysorted(files)
        #print files
        
        s = "<h2>Rule %s</h2>\n" % (d)
        for f in files:
            s += "<img class='bla' src='rules/%s/%s'>\n" % (d,f)
        strings.append(s)
        
    outstr = """
<html>
<head>
<style>
body{ background-color: #eee; }
</style>
</head>
<body>
<h1>Cellular Automata Study</h1>
    %s
</body>
</html>
""" % "\n".join(strings)

    outfile = os.path.join(outdir,"..","rules.html")
    #print outfile
    fp = open(outfile,'w')
    fp.write(outstr)
    fp.close()
          


def foo(rule_nr,outdir,a,rule_study_number,pixel_factor=2):

    # output dir must exist
    path = os.path.join(outdir,"%s"%rule_nr)
    if not os.path.exists(path):
        os.makedirs(path)
    
    ca = Ca()
    
    for i in xrange(rule_study_number):
        # generate random input sequence
        line = []
        while len(line) < a:
            line.append(random.randint(0, 1))
            
        im = ca.getImage(line,rule_nr)
        
        strline = ""
        for j in line: strline += str(j)
            
        #im.save(os.path.join(path,"thumb_%s.png" % (strline)), "PNG")
        
        # enlarge
        im = im.resize((a*pixel_factor,a*pixel_factor), Image.NEAREST)
        im.save(os.path.join(path,"random_%s.png" % strline), "PNG")
    
    

    