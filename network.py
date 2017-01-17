import urllib
#import urllib2
#import cookielib
import http.cookiejar

NETWORK_SPEED_TEST = 0
class Network:
    def __init__(self):
        self.cookiejar = http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        return None
    def open(self,url,postdata=None):
        if postdata is None:
            return self.opener.open(url)
        return self.opener.open(url,postdata)
    def openAndRead(self,url,postdata=None):
        return self.open(url,postdata).read()
    def getText(self,url,postdata=None,encoding='utf-8',errors='ignore'):
        return self.openAndRead(url,postdata).decode(encoding,errors)
    def getpage(url):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        headers = { 'User-Agent':user_agent }
        request = urllib.request.Request(url, headers = headers)
        if NETWORK_SPEED_TEST: print("recieving data")
        response = urllib.request.urlopen(request)
        if NETWORK_SPEED_TEST: print("data recieved")
        return response.read().decode('utf-8','ignore')
