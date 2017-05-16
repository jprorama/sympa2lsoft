#!/usr/bin/python

# get list config from listserv
#
# based on python email examples
# https://docs.python.org/2/library/email-examples.html
import sys
import json
import smtplib
from email.parser import Parser

# loaded from json config for listserv
config=json.load(open("listserv-config.json"))

# sub command
cmd=sys.argv[1]

# list name
lname=sys.argv[2]

# build header
subject = "get list {} {}".format(cmd, lname)

if cmd == "config":
    lcmd = "GET {} (HEADER NOLOCK".format(lname)
elif cmd == "subscribers":
    lcmd = "REVEIW {}".format(lname)

msg = Parser().parsestr('From: {}\n'
                        'To: {}\n'
                        'Subject: {}\n'
                        '\n'
                        '{}\n'.format(config["from"], config["listserv"], subject, lcmd))

print msg.as_string()

# Send the message via our own SMTP server
s = smtplib.SMTP(config["smtp"])
s.sendmail(msg['from'], msg['to'], msg.as_string())
s.quit()
