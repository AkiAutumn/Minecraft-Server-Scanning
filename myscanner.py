import json

from mcstatus import JavaServer
import os
import math
import threading
import time
import argparse

parser = argparse.ArgumentParser(description='get files for procesing')
parser.add_argument("-i", "--inputfile", type=str, help="put in the file with all the server IP's")
parser.add_argument("-o","--outputfile", type=str, help="the name of the file to put in the results")
parser.add_argument("-p","--publicserverlist", type=str, help="put in the file with the public server list (public.txt)")
parser.add_argument("-v","--version", type=str, default="", required=False, help="you can specify the minecarft server you wanna find")
args = parser.parse_args()

masscan = []
print('Multithreaded mass minecraft server status checker by Footsiefat/Deathmonger')

time.sleep(1)

inputfile = args.inputfile
outputfile = args.outputfile
publicserverlist = args.publicserverlist
searchterm = args.version

outfile = open(outputfile, 'a+')
outfile.close

with open(inputfile, 'r') as f:
    json_data = json.load(f)

for server in json_data:
    for attribute, value in server.items():
        if attribute == 'ip':
            masscan.append(value)



def split_array(L,n):
    return [L[i::n] for i in range(n)]


threads = int(input('How many threads do you want to use? (Recommended 20): '))

time.sleep(2)

if len(masscan) < int(threads):
    threads = len(masscan)


split = list(split_array(masscan, threads))

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting Thread " + self.name)
        print_time(self.name)
        print ("Exiting Thread " + self.name)

def print_time(threadName):
    for z in split[int(threadName)]:
        if exitFlag:
            threadName.exit()
        try:
            ip = z
            server = JavaServer.lookup(ip, 25565)
            status = server.status()
            query = server.query()
        except:
            print("Failed to get status of: " + ip)
        else:
            print("Found Server: " + ip)
            print(status.description)


for x in range(threads):
    thread = myThread(x, str(x)).start()