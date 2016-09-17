#!/usr/bin/python



#====================================
# imports
#====================================
import os
from multiprocessing import Process, Queue
import pdserver

print("BITE")
q_cmd_from_pd = Queue()
p =  Process(target=pdserver.start, args=(5001, q_cmd_from_pd))
p.start()

while True:
    cmd_from_pd = q_cmd_from_pd.get()
    print("TOTO: %s" % cmd_from_pd)
