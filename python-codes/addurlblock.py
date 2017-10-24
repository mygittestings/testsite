#!/usr/bin/env python3
import codecs
import sys, getopt



# This script read a text+url text file to produce a jekyll friendly post file for publihsing html

def _isurl(line):

    _urldef = ('http','https','www','ftp')
    if any(x in line for x in _urldef):
        return True
    else:
        return False

def main(argv):

    inputfile = ''

    try:
       opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
       print('-i <inputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('-i <inputfile>')
          sys.exit()
       elif opt in ("-i", "--ifile"):
          inputfile = arg

    fo1 = codecs.open("jekyll.txt","w", encoding="utf-8")
    fo2 = codecs.open("hexo.txt","w", encoding="utf-8")

    with codecs.open(inputfile,'r',encoding="utf-8") as f:
        # print('Opening file: ' + inputfile)
        linecount = 0

        for line in f:
            outline1 = ""
            outline2 = ""

            if line.strip():
                neline = next(f)
                if not neline.strip():
                    if linecount > 0:
                        outline1 = "</div>" + "\n"
                        outline2 = "</div>" + "\n"

                    outline1 = outline1 + "\n&nbsp;\n\n# " + line.strip()
                    outline2 = outline2 + "\n&nbsp;\n\n# " + line.strip()

                    _id = 1

                    outline1 = outline1 + "\n" + "<div id = \"bqdark\" markdown=\"1\">\n"
                    outline2 = outline2 + "\n" + "<div id = \"bqdark\" markdown=\"1\">\n"

                elif _isurl(neline):
                    outline1 = str(_id) + ". [" + line.rstrip() + "]" + "(" + neline.rstrip() + ")" + "{:target=\"_blank\"}\n"
                    outline2 = str(_id) + ". [" + line.rstrip() + "]" + "(" + neline.rstrip() + ")\n"
                    _id = _id + 1
                else:
                    raise ValueError("Something wrong interpratating the above lines")

            linecount = linecount + 1
            fo1.write(outline1) 
            fo2.write(outline2) 

    fo1.write("</div>\n")
    fo2.write("</div>\n")

    f.close()
    fo1.close()
    fo2.close()
    
    # print('Writing file: jekyll.txt')
    # print('Writing file: hexo.txt')


if __name__ == '__main__':
    main(sys.argv[1:])

