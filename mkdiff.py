#!/usr/bin/python

import sys
import re

FILE_DESC="""0a1,3
> /** @file
>  * FIXME.
>  */"""

def printFileDesc():
    print(FILE_DESC)

def printFuncDesc(fname, arg):
    print("> /** " + fname)
    if arg == '' or arg == 'void':
        print(">  * ")
    else:
        for a in arg.split(','):
            tmp = a.lstrip(' \t').rstrip(' \t')
            tokens = tmp.split()
            var = tokens[len(tokens)-1].lstrip('*')
            print(">  * @param " + var + " FIXME")
    print(">  * @return FIXME")
    print(">  */")

if __name__ == '__main__':
    printFileDesc()

    indef = False
    lineno = 0
    pos = 0
    offset = 4
    tmp = ''

    fh = open(sys.argv[1], 'r')
    for line in fh:
        line = line[:-1]
        lineno += 1

        # concatinates multiple lines
        if indef:
            if line != '{':
                tmp += line
                continue
            else:
                line = tmp
                tmp = ''
                indef = False
                
        # single line case
        m1 = re.compile('^(\w+)\(([\w\s,\*\(\)]*)\)$').match(line)
        if m1 != None:
            (fname, arg) = m1.groups()
            if pos == 0:
                pos = lineno - 2

            nlines = 3 + len(arg.split(','))
            print("%da%d,%d" % (pos, pos + offset, pos + offset + (nlines - 1)))
            offset += nlines
            printFuncDesc(fname, arg)
            pos = 0
            continue

        # multiple lines case
        m2 = re.compile('^(\w+)\(([\w\s,\*\(\)]*)').match(line)
        if m2 != None:
            pos = lineno - 2
            indef = True
            tmp = line
