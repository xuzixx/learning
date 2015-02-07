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
    


if __name__ == '__main__':
    logging.warning("begin")



