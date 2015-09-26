# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:16:39 2015

@author: User
"""

#import sys, os
#from contextlib import closing
import pickle
from socket import *
serverHost = 'localhost'
serverPort = 50007


def get_capcha(pic_file_path):
    cap = ""
    try:
        sockobj.send(pickle.dumps(pic_file_path))
        data = sockobj.recv(1024)
        cap = pickle.loads(data)
    except Exception as e:
        print e
    print "capcha = %s" % cap
    return cap

try:
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((serverHost, serverPort))
    #pic_path = os.path.join(os.path.dirname(__file__), 'capcha.png')
    #print pic_path
except Exception as e:
    print "UU server is not available. Please start UU server first."    
    print e