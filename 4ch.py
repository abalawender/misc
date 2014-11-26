# Simple 4chan.org image downloader
#	by Adam Balawender, Nov 26 2014
#
#             for Python 2.7 

import urllib2
import re
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request('http://boards.4chan.org/w/', None, headers)
response = urllib2.urlopen(req)
page = response.read()

links = re.findall("<a href=\"(.{0,80}g)\".{0,80}1920x1080\)", page)
for link in links:
    name = link.split('/')[-1]
    print name
    req  = urllib2.Request( "http:"+link, None, headers)
    res  = urllib2.urlopen(req)
    img  = res.read()
    with open(name, "w") as fd:
        fd.write(img)
