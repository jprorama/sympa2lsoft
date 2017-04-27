#!/usr/bin/python

#
# parse a sympa config file
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
    rectype = fields[0].split(" ", 1)
    if len(fields) == 1:
        defvalue = rectype[1]
        rectype  = rectype[0]
        config[rectype] = defvalue
    else:
        rectype  = rectype[0]
        defvalue = ""
        config[rectype] = {}

        for row in (xrange(1,len(fields))):
            recval = fields[row].split(" ", 1)
            config[rectype][recval[0]] = recval[1]

    # parse owner record
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kOwner
    # The first owner is also editor to act as the default moderatorcnt
    if rectype == "owner":
        print "* Owners=", config[rectype]["email"]
        if ownercnt == 0:
            print "* Editor=", config[rectype]["email"]
            ownercnt = ownercnt + 1

    # parse editor record
    # editors are moderators
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kModerator
    # use ALL keyword to retain semantics so all moderators see requests
    elif rectype == "editor":
        if moderatorcnt == 0:
            print "* Moderator= All,", config[rectype]["email"]
            moderatorcnt = moderatorcnt + 1
        else:
            print "* Moderator= ", config[rectype]["email"]

    # parse subject tagging
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kModerator
    # Will set default to on for lists with SUBJecthdr in Default-options
    elif rectype == "custom_subject":
        print "* Subject-Tag=", config[rectype]

    # parse reply to header
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kReplyTo
    # the semantics don't map completely
    elif rectype == "reply_to_header":
        if config[rectype]["apply"] == "forced":
            p2="ignore"
        else:
            p2=config[rectype]["apply"]

        if config[rectype]["value"] == "all":
            p1="both"
        elif config[rectype]["value"] == "other_email":
            p1=config[rectype]["other_email"]
        else:
            p1=config[rectype]["value"]

        print "* Reply-to=", p1,",", p2

    # parse subscription options
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kSubscription
    # not all models supported, in particular the *_notify feature is not
    # also only support "confirm" option to avoid unintended subscription
    elif rectype == "subscribe":
        if re.search("^open", config[rectype]):
            print "* Subscription: Open,Confirm"
        elif re.search("^owner", config[rectype]):
            print "* Subscription: By_Owner,Confirm"
        elif config[rectype] == "closed":
            print "* Subscription: Closed"

print json.dumps(config, sort_keys=True,indent=4, separators=(',', ': '))
