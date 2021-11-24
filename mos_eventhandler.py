#!/usr/bin/python
# Make sure API is enabled in MOS:
#
# management api
#    no shutdown
#

# Session to API server
from jsonrpclib import Server
import ssl
import json

_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

user='test'
passwd = 'test'
hostname = 'localhost'

device = Server('https://{}:{}@{}/command-api'.format(user, passwd, hostname))

# Reading file to see if we have a cetain match in the logs
import time

def watch(fn, words):
    first_call = True
    fp = open(fn, 'r')
    while True:
        if first_call:
            fp.seek(0, 2)
            first_call = False
        new = fp.readline()
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears

        if new:
            for word in words:
                if word in new:
                    yield (word, new)
        else:
            time.sleep(0.5)

fn = '/var/log/messages'
words = ['up', 'down']
commands = ['show version']

for hit_word, hit_sentence in watch(fn, words):
    # Execute command for every word that matches row in the log
    print "Found %r in line: %r" % (hit_word, hit_sentence)
    result = device.runCmds(1, commands)
    print json.dumps(result, indent=4, sort_keys=True)
