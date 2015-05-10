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

with futures.ProcessPoolExecutor(max_workers = 4) as executor:
    for (x, bytes_sent) in executor.map(count_bytes_sent, filenames):
        x_axis.append(x)
        sum_bytes.append(bytes_sent)

print sum_bytes
"""
max_workers = 4
    real    0m13.461s
    user    0m49.151s
    sys     0m0.613s
"""
