#!/usr/bin/python
# Make sure API is enabled in MOS:
#
# management api
#    no shutdown
#
# Then enable this as daemon:
#
# daemon mos_eventhandler
#    command /mnt/flash/mos_eventhandler.py
#

from jsonrpclib import Server
import ssl
import json

# Configure API variables here:

user='test'
passwd = 'test'
hostname = 'localhost'

# Set up session to API server

_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context


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

# Configure file and command variables here:

fn = '/var/log/messages'
words = ['et41: Port administratively down', 'et41: Port administratively up']
commands_up = ['configure','interface ethernet41', 'description set as up']
commands_down = ['configure','interface ethernet41', 'description set as down']

for hit_word, hit_sentence in watch(fn, words):
    # Execute command for every word that matches row in the log
    print "Found %r in line: %r" % (hit_word, hit_sentence)
    if hit_word == 'et41: Port administratively up':
        result = device.runCmds(1, commands_up)
    if hit_word == 'et41: Port administratively down':
        result = device.runCmds(1, commands_down)