import time

import bzoj_bot
import identify
import grab
from data import Data

global DEBUG; DEBUG = 0

class AutoACMoton:
    def __init__(self):
        if not DEBUG:
            self.contestant = bzoj_bot.BZOJBot()
            self.contestant.login()

    def quit(self):
        if not DEBUG:
            self.contestant.logout()

    def sendheartbeat(self):
        if not DEBUG:
            self.contestant.sendheartbeat()

    ACCESS_DENIED = 1; CANT_FIND_SOLUTIONS = 2; CANT_SUBMIT = 3; HAS_ACCEPTED = -1;
    def solve(self, pid):
        if not self.contestant.can_submit_code(pid):
            print("Please contact lydsy2012@163.com!")
            return self.ACCESS_DENIED
        
        if self.contestant.IsAccepted(Data.username,pid):
            print("problem %d has Accepted, skiping..." % pid)
            return self.HAS_ACCEPTED

        sols = grab.grab_from_baidu_page("bzoj%d" % pid)
        print('got solution list')
        for sid, sol in enumerate(sols):
            sol_code = grab.grab_code(sol)
            if len(sol_code['code']) == 0 or not identify.iscpp(sol_code['code'][0]): continue
            print('get solution %d. sending...' % (sid+1))
            if DEBUG:
                print(sol_code['code'][0])
                break
            else:
                response = self.contestant.submit_code(pid, sol_code['code'][0])
                result = self.contestant.getresult(pid)
                if result == '': return self.CANT_SUBMIT
                print("solution%d: %s" % (sid+1, result))
                if result == 'Accepted':
                    source_file = open("bzoj/P%d.cpp" % pid, "w")
                    source_file.write(sol_code['code'][0])
                    source_file.close()
                    return 0
                time.sleep(6)
        return self.CANT_FIND_SOLUTIONS
