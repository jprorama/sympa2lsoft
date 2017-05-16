#!/usr/bin/python

#
# parse a sympa config file to json
#

import fileinput
import re
import json

ownercnt=0
moderatorcnt=0

# record generator for sympa config file
# each record is separated by blank lines
# records are returned one record at a time
def record(file):
    currec = ""
    # uncomment for parse debug
    # linecnt = 0
    found = False # skip leading blank lines in file
    for line in file:
        # uncomment for parse debug
        # linecnt =+ linecnt + 1
        line = line.lstrip().rstrip("\n")
        if re.search("^$", line):
            if found:
                if currec:
                    # only yeild records for non-blank lines
                    yield currec
                    # uncomment for parse debug
                    # print "{}: {}".format(linecnt, currec)
                    currec = ""
                else:
                    # skip blank lines
                    currect = ""
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
    rectype = fields[0].split(" ", 1)
    if len(fields) == 1:
        defvalue = rectype[1]
        rectype  = rectype[0]
        config[rectype] = defvalue
    else:
        rectype  = rectype[0]
        defvalue = ""
        tmp = {}

        # build dictionary of fields in record
        for row in (xrange(1,len(fields))):
            recval = fields[row].split(" ", 1)
            tmp[recval[0]] = recval[1]

        # if a config exists convert to list of entries
        if rectype in config:
            if type(config[rectype]).__name__ == "dict":
                # turn it into a list an
                config[rectype] = [ config[rectype] ]
            config[rectype].append( tmp )
        else:
            config[rectype] = tmp

print json.dumps(config, sort_keys=True,indent=4, separators=(',', ': '))
