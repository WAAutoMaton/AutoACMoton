import network,re;

def IsAccepted(username,problemID):
    page=network.getpage("http://www.lydsy.com/JudgeOnline/userinfo.php?user=%s" % username)
    pattern=re.compile("p\\(%d\\)(.*)</script>" % problemID)
    return re.search(pattern,page)



