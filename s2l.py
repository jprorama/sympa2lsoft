#!/usr/bin/python

#
# parse a sympa config file
#

import fileinput
import re

# record generator for sympa config file
# each record is separated by blank lines
# records are returned one record at a time
def record(file):
    currec = ""
    found = False # skip leading blank lines in file
    for line in file:
        line = line.rstrip("\n")
        if re.search("^$", line):
            if found:
                yield currec
                currec = ""
            else:
                next
        else:
            found = True
            if currec:
                currec = currec + "\n" + line
            else:
                currec = line

# process config file one record at a time
i=0
for rec in record(fileinput.input()):
    i = i + 1
    print "record", i
    # parse record type and value for one line records
    fields = rec.split('\n')
    rectype = fields[0].rsplit(" ")
    if len(rectype) == 2:
        rectype  = rectype[0]
        defvalue = rectype[1]
    else:
        rectype  = rectype[0]
        defvalue = ""

    print rectype
    print rec
    print
