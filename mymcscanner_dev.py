import csv
from datetime import datetime
import json

from mcstatus import JavaServer
import os
import threading
import time
import argparse

os.system('color')  # Color support for terminal

parser = argparse.ArgumentParser(description='get files for procesing')
parser.add_argument("-i", "--inputfile", type=str, help="put in the file with all the server IP's")
parser.add_argument("-o", "--outputfile", type=str, help="the name of the file to put in the results")
parser.add_argument("-p", "--publicserverlist", type=str,
                    help="put in the file with the public server list (public.txt)")
parser.add_argument("-v", "--version", type=str, default="", required=False,
                    help="you can specify the minecarft server you wanna find")
args = parser.parse_args()

masscan = []
print('Multithreaded mass minecraft server status checker by Footsiefat/Deathmonger')

time.sleep(1)

inputfile = args.inputfile
outputfile = args.outputfile
publicserverlist = args.publicserverlist
searchterm = args.version

outfile = open(outputfile, 'a')
outfile.close

with open(inputfile, 'r') as f:
    json_data = json.load(f)

for server in json_data:
    for attribute, value in server.items():
        if attribute == 'ip':
            masscan.append(value)


def split_array(L, n):
    return [L[i::n] for i in range(n)]


threads = int(input('How many threads do you want to use? (Recommended 20): '))

time.sleep(2)

if len(masscan) < int(threads):
    threads = len(masscan)

split = list(split_array(masscan, threads))

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting Thread " + self.name)
        print_time(self.name)
        print("Exiting Thread " + self.name)


def print_time(threadName):
    for ip in split[int(threadName)]:
        if exitFlag:
            threadName.exit()
        try:
            serverino = JavaServer.lookup(ip, 25565)
            status = serverino.status()
        except:
            print(bcolors.LightRed + ip + " didn't respond" + bcolors.Default)
        else:
            with open(outputfile, encoding="UTF8") as f:
                if ip not in f.read():
                    print(bcolors.LightMagenta + "Found Server: " + ip + ":25565" + bcolors.Default)
                    print(status.description)

                    now = datetime.now()  # current date and time
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

                    data = [date_time, ip + ":25565", status.version.name, status.description, status.players.max]

                    # write to output
                    csv_file = open(outputfile, 'a', encoding='UTF8', newline='')
                    writer = csv.writer(csv_file)
                    writer.writerow(data)
                else:
                    print(bcolors.LightBlue + "Skipped " + ip + bcolors.Default)


for x in range(threads):
    thread = myThread(x, str(x)).start()

class bcolors:
    ResetAll = "\033[0m"

    Bold = "\033[1m"
    Dim = "\033[2m"
    Underlined = "\033[4m"
    Blink = "\033[5m"
    Reverse = "\033[7m"
    Hidden = "\033[8m"

    ResetBold = "\033[21m"
    ResetDim = "\033[22m"
    ResetUnderlined = "\033[24m"
    ResetBlink = "\033[25m"
    ResetReverse = "\033[27m"
    ResetHidden = "\033[28m"

    Default = "\033[39m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"

    BackgroundDefault = "\033[49m"
    BackgroundBlack = "\033[40m"
    BackgroundRed = "\033[41m"
    BackgroundGreen = "\033[42m"
    BackgroundYellow = "\033[43m"
    BackgroundBlue = "\033[44m"
    BackgroundMagenta = "\033[45m"
    BackgroundCyan = "\033[46m"
    BackgroundLightGray = "\033[47m"
    BackgroundDarkGray = "\033[100m"
    BackgroundLightRed = "\033[101m"
    BackgroundLightGreen = "\033[102m"
    BackgroundLightYellow = "\033[103m"
    BackgroundLightBlue = "\033[104m"
    BackgroundLightMagenta = "\033[105m"
    BackgroundLightCyan = "\033[106m"
    BackgroundWhite = "\033[107m"
