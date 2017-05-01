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

msg = Parser().parsestr('From: {}\n'
                        'To: {}\n'
                        'Subject: get list config {}\n'
                        '\n'
                        'GET {} (HEADER NOLOCK\n'.format(config["from"], config["listserv"], sys.argv[1], sys.argv[1]))

print msg.as_string()

# Send the message via our own SMTP server
s = smtplib.SMTP(config["smtp"])
s.sendmail(msg['from'], msg['to'], msg.as_string())
s.quit()
