#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import glob
from concurrent import futures
from collections import Counter

from errcode.models import LogInfo
from errcode.tool import *

@test_timer
def single_thread_ex():
    """ 单线程 """
    counter = Counter()
    for filename in glob.glob("../log/access.log.*"):
        with open(filename) as f:
            for line in f:
                try:
                    log_info = LogInfo(line)
                    counter[log_info.url] += 1
                except:
                    pass

    for path, count in counter.most_common(10):
        print "%s [%s]" % (count, path)

def count_urls(filename):
    """ 多线程/进程 调用方法 """
    counter = Counter()
    with open(filename) as f:
        for line in f:
            try:
                log_info = LogInfo(line)
                counter[log_info.url] += 1
            except:
                pass
    return counter

@test_timer
def multi_process_ex():
    merged_counter = Counter()
    filenames = glob.glob("../log/access.log.*")

    with futures.ProcessPoolExecutor(max_workers  = 4) as executor:
        for counter in executor.map(count_urls, filenames):
            merged_counter.update(counter)

    for path, count in merged_counter.most_common(10):
        print "%s [%s]" % (count, path)

if __name__ == "__main__":
    print "----test"
    single_thread_ex()
    print "----test"
    multi_process_ex()

    """
    test [single_thread_ex] used : 26.877772
    test [multi_process_ex] used : 1.345392
    """
