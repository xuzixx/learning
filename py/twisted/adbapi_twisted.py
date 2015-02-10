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
    filename= __file__ + ".log",
    level = logging.WARNING,
    format='%(asctime)s - %(levelname)s (%(threadName)-10s) %(message)s',)

dbpool = adbapi.ConnectionPool("MySQLdb", 
    db = 'test', 
    user = 'root', 
    passwd = 'wxtest', 
    port = 3306, 
    host = 'localhost', 
    cp_max = 100) #连接数配置

def main_db(list = []):
    count = 0 
    while True:
        item = "2014-01-01:%s: %s" % (datetime.datetime.now(), count)
        #d = dbpool.runQuery("select * from t_servic where svc_id = %s", 10037)
        #d = dbpool.runInteraction(test_db,item)
        d = dbpool.runInteraction(insert_db,item)
        #d.addCallbacks(test_callback, test_errback)
        count = count + 1
        if count == 10000000:
            break
    # 会不会 一个defer 没做完？
    # 运行状态是 end 很早就被打印出来了，但是还是等待了所有的defer都运行完才执行的stop
    logging.warning("end")
    reactor.stop()

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
        txn.execute(insert_sql)
        logging.warning("done:"+line)
        return None
        #result = txn.fetchall() # insert fech出来是None
        #if result:
        #    return result
        #else:
        #    return None
    except:
        logging.warning("failed:"+line)
        #print traceback.format_exc()
        return None

if __name__ == '__main__':
    logging.warning("begin")
    reactor.suggestThreadPoolSize(10)
    threads.deferToThread(main_db)
    reactor.run()

"""
一千万数据 入库 90分钟
"""

