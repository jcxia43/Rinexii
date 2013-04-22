#!/usr/bin/python

import sys
try:
    f = open(sys.argv[1],'r')
    print "File exist."
except:
    print "No file"
