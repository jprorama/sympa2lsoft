#!/usr/bin/python

#
# parse a sympa json config file to lsoft
#

import sys
import re
import json

ownercnt=0
moderatorcnt=0

# loaded from json input
config=json.load(sys.stdin)

for rectype in sorted(config.keys()):
    # parse owner record
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kOwner
    # The first owner is also editor to act as the default moderatorcnt
    if rectype == "owner":
        if type(config[rectype]).__name__ == "dict":
            print "* Owners= {}".format(config[rectype]["email"])
            print "* Editor= {}".format(config[rectype]["email"])
        else:
            for i in range(0, len(config[rectype])):
                print "* Owners= {}".format(config[rectype][i]["email"])
                if ownercnt == 0:
                    print "* Editor= {}".format(config[rectype][i]["email"])
                    ownercnt = ownercnt + 1


    # parse editor record
    # editors are moderators
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kModerator
    # use ALL keyword to retain semantics so all moderators see requests
    elif rectype == "editor":
        if type(config[rectype]).__name__ == "dict":
            print "* Moderator= {}".format(config[rectype]["email"])
        else:
            for i in range(0, len(config[rectype])):
                if moderatorcnt == 0:
                    print "* Moderator= All,{}".format(config[rectype][i]["email"])
                    moderatorcnt = moderatorcnt + 1
                else:
                    print "* Moderator= {}".format(config[rectype][i]["email"])

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

        print "* Reply-to= {},{}".format(p1,p2)

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

    # parse the review permission
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#kReview
    # relies on the access-level values which are a superset of sympa
    # http://www.lsoft.com/manuals/16.0/listkeyw.html#bGeneric
    elif rectype == "review":
        print "* Review= {}".format(config[rectype])

# default options for modern Internet lists
# http://www.lsoft.com/manuals/16.0/listkeyw.html#kDefaultOptions
# users get a copy of their own messages
# they don't need to confirm to post
# Subject tagging is default
print "* Default-options: REPRO,NOACK,SUBJecthdr"

# http://www.lsoft.com/manuals/16.0/listkeyw.html#kMailMerge
print "* Mail-Merge= No"
