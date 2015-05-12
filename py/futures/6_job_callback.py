#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import socket
from concurrent import futures

ip_addresses = ['8.8.8.8','61.135.132.59','8.8.8.8','61.135.132.59','8.8.8.8','61.135.132.59','8.8.8.8','61.135.132.59','8.8.8.8','61.135.132.59','8.8.8.8','61.135.132.59']

def resolve_fqdn(ip_addr):
    fqdn = socket.getfqdn(ip_addr)
    return ip_addr, fqdn

def print_mapping(job):
    ip_addr, fqdn = job.result()
    print ip_addr, fqdn

with futures.ProcessPoolExecutor(max_workers = 2) as executor:
    for ip_addr in ip_addresses:
        job = executor.submit(resolve_fqdn, ip_addr)
        job.add_done_callback(print_mapping)

"""
Technical notes: 
    The callback occurs in the same process which submitted the job, which is exactly what's needed here. 
    However, the documentation doesn't say that all of the callbacks will be done from the same thread, 
    so if you are using a thread pool then you probably want to use a thread lock around a shared resource.
    (sys.stdout is a shared resource, so you would need one around the print statement here. 

    I'm using a process pool, and the concurrent process pool implementation uses a single local worker thread, 
    so I don't think I have to worry about contention. You should verify that.)
"""
