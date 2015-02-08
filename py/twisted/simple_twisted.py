#coding=utf-8
#import MySQLdb

from twisted.python import threadable
threadable.init(1)
from twisted.internet import threads, reactor,defer

import random
import time
import logging
import traceback
import datetime


logging.basicConfig(
    filename= __file__ + ".log",
    level = logging.WARNING,
    format='%(asctime)s - %(levelname)s (%(threadName)-10s) %(message)s',)

def main(list = "",func = "",call_back = ""):
    deferlist = []
    for item in list:
        d = threads.deferToThread(func,item)
        d.addCallbacks(test_call_back, test_error_back)
        deferlist.append(d)
    # 数组会超级大 
    deferlist.append(d)

    #dl = defer.DeferredList(deferlist, consumeErrors = True)
    #dl = defer.DeferredList(deferlist, consumeErrors = True, fireOnOneErrback = 1)
    dl = defer.DeferredList(deferlist, fireOnOneErrback = 1)
    dl.addCallback(test_dl_call_back)
    dl.addErrback(test_dl_error_back) #标准的DeferredList不会调用errback
    dl.addBoth(call_back)
    
#test func
def test_print_line(line):
    print line.strip()
    time.sleep(random.randint(1, 2))
    if line == '2':
        raise Exception
    #logging.warning(line)
    return line #需要有return 才能触发main_db 中的reactor.stop
    #pass

def test_call_back(result):
    print "---test_call_back : %s" % result

def test_error_back(result):
    print "---test_error_back"
    print type(result)
    print "class:[%s]" % result.__class__
    print result
    print "---test_error_end"

def test_dl_both_back(result):
    print "---test_dl_both_back"
    print result
    reactor.stop()
    print "%s" % datetime.datetime.now()

def test_dl_call_back(result):
    print "---test_dl_call_back"
    print result

def test_dl_error_back(result):
    print "---test_dl_error_back"
    print type(result)
    print result.__class__
    print result
    print "---test_dl_error_end"

if __name__ == '__main__':
    logging.warning("begin")
    print "%s" % datetime.datetime.now()
    list = ["1","2","3","4","5","6"]
    main(list = list, func = test_print_line, call_back = test_dl_both_back)
    reactor.suggestThreadPoolSize(2)
    reactor.run()

"""
场景：有时候我们需要在几个不同的事件都发生了才被通知，而不是分别等待每个事件。例如，我们可能需要等待一个列表中的连接全部关闭。
使用：twisted.internet.defer.DeferredList

"""






