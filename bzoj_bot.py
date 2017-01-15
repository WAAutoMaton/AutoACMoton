import re
import time
import urllib
import http.cookiejar

import processor
import identify
from data import Data
class BZOJBot:
    def __init__(self):
        self.cookiejar = http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        return None

    def login(self):
        loginurl = 'http://www.lydsy.com/JudgeOnline/login.php'
        postdata = urllib.parse.urlencode({ 
                    'user_id':Data.username, 
                    'password':Data.password }).encode('utf-8')
        self.opener.open(loginurl, postdata)

    def logout(self):
        logouturl = 'http://www.lydsy.com/JudgeOnline/logout.php'
        self.opener.open(logouturl)
    
    def sendheartbeat(self):
        self.opener.open('http://www.lydsy.com/JudgeOnline/')

    def submit_code(self, pid, code):
        submiturl = 'http://www.lydsy.com/JudgeOnline/submit.php'
        postdata = urllib.parse.urlencode({
                    'id':pid,
                    'language':'1', #iscpp
                    'source':code }).encode('utf-8')
        return self.opener.open(submiturl, postdata).read()

    def can_submit_code(self, pid):
        problemurl = 'http://www.lydsy.com/JudgeOnline/problem.php?id=%d' % pid
        problem_page = self.opener.open(problemurl).read().decode('utf-8')
        if identify.isproblempage(problem_page):return True
        return False

    def getresult(self, pid):
        expr_status_f = 'Accepted|Presentation_Error|Wrong_Answer|Time_Limit_Exceed|Memory_Limit_Exceed|Output_Limit_Exceed|Runtime_Error|Compile_Error'
        url = 'http://www.lydsy.com/JudgeOnline/status.php?user_id=%s&problem_id=%d' % (Data.username, pid)

        print('judging...')
        page = self.opener.open(url).read().decode('utf-8')
        statu = processor.getfirstresult(page)
        cnt = 0
        while not re.match(expr_status_f, statu):
            ++cnt
            if(cnt>130):
                statu = ''
                break
            time.sleep(1)
            page = self.opener.open(url).read().decode('utf-8')
            statu = processor.getfirstresult(page)
        return statu

