#!/bin/env pyhon
#coding=utf-8
import os, sys
sys.path.append("..")
import time
import traceback

#from config import *

"""
01. msec                       = "访问时间和时区（日志时间戳）"
02. request_time               = 请求处理时长（ms）
03. remote_addr                = "客户端地址"
04. upstream_cache_status      = "缓存的命中状态"
05. status                     = "响应状态代码"
06. bytes_sent                 = "返回客户端的内容长度"
07. request_method             = "请求方式"
08. scheme                     = "请求模式，htttp，https"
09. host                       = "请求服务器"
10. request_uri                = "请求URI"
11. upstream_addr              = "后台upstream的地址，即真正提供服务的主机地址"
12. upstream_http_content_type = "内容类型"
13. http_refer                 = "跳转来源"
14. http_user_agent            = "用户终端代理"

ex:
    正常:
    'zz_11_22 fssnginx[10369]: 1425279601.506 0.000 123.8.183.220 -/200 8929 GET http://photocdn.abcd.com/20111230/vrs418210_Ne7rQ_pic23.jpg - DIRECT/10.37.11.60:80 image/jpeg "http://tv.abcd.com/20140228/n395827560.shtml?txid=5f03d2e3f55a51cbcdcb2fa741620385" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"'
    错误:
    '00:59:00 tc_128_34 fssnginx[1040]: 1425574740.332 59.521 107.178.200.199 -/499 0 GET http://api.t.abcd.com/statuses/comments_timeline.json?count=20&source=5vi74qXPB5J97GNzsevN&nocache=1425574584159 - DIRECT/10.11.152.73:80 - "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36 AppEngine-Google; (+http://code.google.com/appengine; appid: s~memoryfirstgae)"'
"""

class LogInfo():
    def __init__(self, function_log_line):
        """ init 应该需要 给status refer url默认值"""
        self.url = ""
        self.refer = ""
        self.status = 0
        try:
            _, _, self.msec, self.request_time, self.remote_addr, \
            tmp_status, self.bytes_sent, self.request_method, \
            tmp_tail = function_log_line.strip('\n').split(" ",8)

            self.upstream_cache_status, self.status = tmp_status.split("/")
            # 如果只是按空格区分，有的url中包含空格，会导致后面错误
            tmp_url, tmp_tail = tmp_tail.split(" - DIRECT/",1)
            self.url = tmp_url.split('?')[0]
            self.upstream_addr, tmp_tail = tmp_tail.split(" ",1)
            tmp_http_refer = tmp_tail.split('"')[1]
            self.refer = tmp_http_refer.split("?")[0]

            #if(isinstance(self.msec, float)):
            #    pass
            #else:
            #    #raise LogInfoException("[init error]msec error")
            #    print "after raise"
        except Exception, e:
            raise LogInfoException(function_log_line)
            # TEST:
            #print function_log_line
            #exstr = traceback.format_exc()
            #print exstr
        
    def show_info(self):
        print "[LogInfo]--------%s" % id(self)
        for i,key in enumerate(self.__dict__):
            print "[%s,%s] %s" %(i, key, self.__dict__[key]) 
            
    def get_error_code_key(self):
        return "%s|%s" % (self.url, self.status)


class LogInfoException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "[LogInfoException]:%s" % self.msg

if __name__ == "__main__":
#    error_line = '00:59:00 tc_128_34 fssnginx[1040]: 1425574740.332 59.521 107.178.200.199 -/499 0 GET http://api.t.abcd.com/statuses/comments_timeline.json?count=20&source=5vi74qXPB5J97GNzsevN&nocache=1425574584159 - DIRECT/10.11.152.73:80 - "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36 AppEngine-Google; (+http://code.google.com/appengine; appid: s~memoryfirstgae)"'
    line = 'zz_11_22 fssnginx[10369]: 1425279601.506 0.000 123.8.183.220 -/200 8929 GET http://photocdn.abcd.com/20111230/vrs418210_Ne7rQ_pic23.jpg - DIRECT/10.37.11.60:80 image/jpeg "http://tv.abcd.com/20140228/n395827560.shtml?txid=5f03d2e3f55a51cbcdcb2fa741620385" "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"'
    log_info = LogInfo(line)
    log_info.show_info()
    print log_info.get_error_code_key()


