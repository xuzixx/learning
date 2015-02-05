#coding=utf-8
#import MySQLdb

from twisted.python import threadable
threadable.init(1)
from twisted.internet import threads, reactor,defer
from twisted.enterprise import adbapi

import random
import time
import logging
import traceback
import datetime

logging.basicConfig(
    filename="twisted.log",level = logging.WARNING,format='%(asctime)s - %(levelname)s (%(threadName)-10s) %(message)s',)

dbpool = adbapi.ConnectionPool("MySQLdb", 
    db = 'test', user = 'root', passwd = 'wxtest', port = 3306, host = 'localhost', cp_max = 50)

def main(list = "",func = "",call_back = ""):
    deferlist = []
    for item in list:
        d = threads.deferToThread(func,item)
        deferlist.append(d)
    # 数组会超级大 
    #d = threads.deferToThread(func,"done")
    #deferlist.append(d)

    dl = defer.DeferredList(deferlist)
    #dl.addCallback(test_call_back)
    dl.addErrback(test_error_back) # 应该测试一下db raise error
    dl.addBoth(test_both_back)
    
def line_reader(filename):
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                f.close()
                break
            yield line
def main_db(filename = ""):
    reader = line_reader(filename)
#    for line in reader:
    line = reader.next()
    count = 0
    while line:
        #d = dbpool.runQuery("select * from t_servic where svc_id = %s", 10037)
        #d = dbpool.runInteraction(test_db,item)
        d = dbpool.runInteraction(insert_db,line)
        #d.addCallbacks(test_callback, test_errback)
        #print d.__class__
        #d.cancel()
        #print count
        count = count + 1
        if count == 10000000:
            break
       
#        line = None
        #d = threads.deferToThread(test_print_line,line) #测试通过，可以多个defer

    #会不会 一个defer 没做完？
    logging.warning("end")
    reactor.stop()
def test_callback(res):
    pass
    #print res
def test_errback(err):
    #print "error got:", err
    pass

    

#dbpool.runInteraction 默认就传了第一参数
def test_db(txn, item):
    # 应该是不可以 替换
    #time.sleep(random.randint(1, 5))
    txn.execute('select * from t_service where svc_id = %s' % "10037")
    result = txn.fetchall() 
    logging.warning(result[0][0])
    if result:
        return result
    else:
        return None

def insert_db(txn, line):
    line = line.strip()
    try:
        tmp = line.split(":")
        date = tmp[0]
        flow = tmp[-1]
        del tmp[0]
        del tmp[-1]
        domain = "".join(tmp)
        param = (date, domain, flow)
        insert_sql = "insert into dmflow_day_2014 (time, domain, len) values ('%s', '%s', '%s')" % param
        #insert_sql = "insert into dmflow_day_2014_test (time, domain, len) values ('%s', '%s', '%s')" % param
        txn.execute(insert_sql)
        logging.warning("done:"+line)
        return None #一开始没有return None 是否是不释放的原因？
        #result = txn.fetchall() # insert fech出来是None
        #if result:
        #    return result
        #else:
        #    return None
    except:
        logging.warning("failed:"+line)
        #print traceback.format_exc()
        return None
    
#test func
def test_print_line(line):
    print line.strip()
    time.sleep(random.randint(1, 5))
    logging.warning(line)
    return None #需要有return 才能触发main_db 中的reactor.stop
    #pass

def test_both_back(result):
    print "--both"
    print result
    reactor.stop()
    print "%s" % datetime.datetime.now()

def test_call_back(result):
    print "---success"
    print result

def test_error_back(result):
    print "----error"
    print result

if __name__ == '__main__':
    logging.warning("begin")
#    with open('2014_result.txt') as file:
#    with open('sql.txt') as file:
#        file = ["2014-10-24:www.baidu.com:2000","2014-01-01:s1.biz.itc.cn:419092"]
        #main(list = file,func = test_print_line, call_back = test_call_back)
        #main(list = file,func = test_db, call_back = test_call_back)
        #main_db(list = file)
    reactor.suggestThreadPoolSize(10)
#        reactor.callInThread(main_db, list = file) #这么调用，特么 一直只有5个线程
    threads.deferToThread(main_db, filename = "sql.txt")
    reactor.run()



