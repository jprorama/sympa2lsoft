#!/usr/bin/python

#
# parse a sympa config file
#

import fileinput
import re
import json

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
config={}
for rec in record(fileinput.input()):
    # parse record type and value for one line records
    fields = rec.split('\n')
    rectype = fields[0].rsplit(" ")
    if len(rectype) == 2:
        rectype  = rectype[0]
        defvalue = rectype[1]
        config[rectype] = defvalue
    else:
        rectype  = rectype[0]
        defvalue = ""
        config[rectype] = {}

        for row in (xrange(1,len(fields))):
            recval = fields[row].split(" ")
            config[rectype][recval[0]] = recval[1]

print json.dumps(config, sort_keys=True,indent=4, separators=(',', ': '))
