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

            if line.strip(): # start with non-empty lines
                neline = next(f)
                if not neline.strip(): # if empty next line -> section header
                    if linecount > 0:
                        outline1 = "</div>" + "\n"
                        outline2 = "</div>" + "\n"

                    outline1 = outline1 + "\n&nbsp;\n\n# " + line.strip()
                    outline2 = outline2 + "\n&nbsp;\n\n# " + line.strip()

                    _id = 1

                    outline1 = outline1 + "\n" + "<div id = \"bqdark\" markdown=\"1\">\n"
                    outline2 = outline2 + "\n" + "<div id = \"bqdark\" markdown=\"1\">\n"

                elif _isurl(neline): # if valid url next line -> source

                    outline1 = str(_id) + ". [" + line.rstrip() + "]" + "(" + neline.rstrip() + ")" + "{:target=\"_blank\"}"
                    outline2 = str(_id) + ". [" + line.rstrip() + "]" + "(" + neline.rstrip() + ")"

                    placeholder = " " * len(str(_id))

                    neneline=next(f)
                    while neneline.strip(): # all consecutive lines under a source are treated as urls
                        if not _isurl(neneline):
                            print(neneline + " not an url: skipped")
                            continue

                        sourcename = ""
                        if "youku" in neneline:
                            sourcename = "优酷"
                        elif "iqiyi" in neneline:
                            sourcename = "爱奇艺"
                        elif "tudou" in neneline:
                            sourcename = "土豆"
                        elif "v.qq.com" in neneline:
                            sourcename = "腾讯"
                        elif "youtube" in neneline:
                            sourcename = "油管"
                        else:
                            sourcename = "其它"
                            #emsg = "Unknown video source: \n" + neneline
                            #raise ValueError(emsg) 

                        outline1 = outline1 + ", " + placeholder + "   [" + sourcename + "]" + "(" + neneline.rstrip() + ")" + "{:target=\"_blank\"}"
                        outline2 = outline2 + "," + placeholder + "   [" + sourcename + "]" + "(" + neneline.rstrip() + ")"
                        neneline=next(f)

                    outline1 = outline1 + "\n"
                    outline2 = outline2 + "\n"
                    _id = _id + 1

                else: # if not section header nor a source with a valid url
                    print("Error at line: " + line)
                    raise ValueError("Only one line is allowed for each section header")

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

