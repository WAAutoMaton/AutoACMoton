#!/usr/bin/env python3
import sys
import getopt
import time

import auto_ACmoton
from data import Data

try:
    options,args = getopt.getopt(sys.argv[1:], 'hs:t:u:p:', ['help', 'start=', 'interval=','username=','password='])
except getopt.GetoptError:
    sys.exit()

for option,value in options:
    if option in ('-s', '--start'):
        start_pid = int(value)
    if option in ('-t', '--interval'):
        interval = int(value)
    if option in ('-u', '--username'):
        Data.username = str(value)
    if option in ('-p', '--password'):
        Data.password = str(value)
a = auto_ACmoton.AutoACMoton()

pid = start_pid

while True:
    print('==========solving problem %d==========' % pid)
    code = a.solve(pid)
    if code != 0:
        print("can not solve problem %d, ErrorCode: %d" % (pid, code))
        pid = pid + 1
        continue
    pid = pid + 1
    interval_minute=int(interval/60)
    interval_second=int(interval%60)
    for i in range(interval_minute):
        a.sendheartbeat()
        time.sleep(60)
    time.sleep(interval_second)
