import re
import time
import urllib
import http.cookiejar

import processor
import identify
from data import Data
from network import Network
class BZOJBot:
    network = Network()
    def __init__(self):
        return None

    def login(self):
        loginurl = 'http://www.lydsy.com/JudgeOnline/login.php'
        postdata = urllib.parse.urlencode({ 
                    'user_id':Data.username, 
                    'password':Data.password }).encode('utf-8')
        self.network.open(loginurl, postdata)

    def logout(self):
        logouturl = 'http://www.lydsy.com/JudgeOnline/logout.php'
        self.network.open(logouturl)
    
    def sendheartbeat(self):
        self.network.open('http://www.lydsy.com/JudgeOnline/')

    def submit_code(self, pid, code):
        submiturl = 'http://www.lydsy.com/JudgeOnline/submit.php'
        postdata = urllib.parse.urlencode({
                    'id':pid,
                    'language':'1', #iscpp
                    'source':code }).encode('utf-8')
        return self.network.openAndRead(submiturl, postdata)

    def can_submit_code(self, pid):
        problemurl = 'http://www.lydsy.com/JudgeOnline/problem.php?id=%d' % pid
        problem_page = self.network.getText(problemurl)
        if identify.isproblempage(problem_page):return True
        return False

    def getresult(self, pid):
        expr_status_f = 'Accepted|Presentation_Error|Wrong_Answer|Time_Limit_Exceed|Memory_Limit_Exceed|Output_Limit_Exceed|Runtime_Error|Compile_Error'
        url = 'http://www.lydsy.com/JudgeOnline/status.php?user_id=%s&problem_id=%d' % (Data.username, pid)

        print('judging...')
        page = self.network.getText(url)
        statu = processor.getfirstresult(page)
        cnt = 0
        while not re.match(expr_status_f, statu):
            ++cnt
            if(cnt>130):
                statu = ''
                break
            time.sleep(1)
            page = self.network.getText(url)
            statu = processor.getfirstresult(page)
        return statu
    def isAC(self, pid):
        url='http://www.lydsy.com/JudgeOnline/userinfo.php?user=%s' % Data.username
