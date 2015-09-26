# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:13:04 2015

@author: User
"""

from socket import *
from contextlib import closing
import time
import pickle
import uuModule
myHost = ''
myPort = 50007

def process_request(capcha_path): 
    start = time.time()
    print "Processing: %s" % capcha_path
    cap = ""

    try:
        cap = uuModule.getCapcha(capcha_path)
    except Exception as e:
        print e
    end = time.time()
    print "Time elapsed: %s s" % (end-start)
    return cap
    
with closing(socket(AF_INET, SOCK_STREAM)) as sockobj:
    sockobj.bind((myHost, myPort))
    sockobj.listen(5)
    #uuModule.initializeUU()
    while True:
        try:
            connection, address = sockobj.accept()
            print 'Client connected: ', address
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                result = process_request(pickle.loads(data))
                connection.send(pickle.dumps(result))
            connection.close()
            print 'Client disconnected: ', address
        except Exception as e:
            print e

raw_input("Press any key to quit.")