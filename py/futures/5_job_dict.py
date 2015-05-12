#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import socket
from concurrent import futures

ip_addresses = ['8.8.8.8','61.135.132.59']

with futures.ProcessPoolExecutor(max_workers = 2) as executor:
    jobs = {}
    for ip_addr in ip_addresses:
        job = executor.submit(socket.getfqdn, ip_addr)
        jobs[job] = ip_addr

    # get the completed jobs wherever they are done
    for job in futures.as_completed(jobs):
        ip_addr = jobs[job]
        fqdn = job.result()
        print ip_addr, fqdn

