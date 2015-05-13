#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import ConfigParser

import urllib2, urllib
import cookielib

cf = ConfigParser.ConfigParser()
cf.read("conf.log")

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
opener.open(cf.get("web_info","url"))

print "----cookie"
print cookie
print "----dir cookie"
print dir(cookie)
print "----value cookie"
for ck in cookie:
    print "%s : %s" % (ck.name, ck.value)


login_url = "%s/loginController/login" % cf.get("web_info","url")
login_data = urllib.urlencode({"userName":cf.get("web_info","userName"),"password":cf.get("web_info","password")})

opener.open(login_url, login_data)

print "----value cookie"
for ck in cookie:
    print "%s : %s" % (ck.name, ck.value)

get_url = "http://net.no.sohu.com:8080/netmonitor/cdnController/vmsSingle"
print opener.open(get_url).read()
