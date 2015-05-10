#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import glob
from concurrent import futures

from errcode.models import LogInfo

def count_bytes_sent(filename):
    bytes_sent = 0
    with open(filename) as f:
        for line in f:
            try:
                log_info = LogInfo(line)
                bytes_sent += int(log_info.bytes_sent)
            except:
                pass
    x = filename.split(".")[-1]
    return (x, bytes_sent)

filenames = glob.glob("../log/access.log.*")

x_axis = []
sum_bytes = []

with futures.ThreadPoolExecutor(max_workers = 2) as executor:
    for (x, bytes_sent) in executor.map(count_bytes_sent, filenames):
        x_axis.append(x)
        sum_bytes.append(bytes_sent)

print sum_bytes
"""
max_workers = 2
    real    0m30.788s
    user    0m29.251s
    sys     0m5.605s
max_workers = 3
    real    0m31.445s
    user    0m29.740s
    sys     0m6.260s
max_workers = 4
    real    0m31.601s
    user    0m29.876s
    sys     0m6.164s
"""

# TEST: 由于日志不是日期格式，所以不能出图
#from pylab import *
#plot(x_axis, sum_bytes)
#ylim(0, max(sum_bytes))
#title("2 test ThreadPool")
#savefig("png/2_thread_pool.png")
