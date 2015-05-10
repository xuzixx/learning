#!/bin/env pyhon
#coding=utf-8
import os, sys
sys.path.append("..")
import time
import functools

def test_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        result = func(*args, **kwargs)
        end = time.clock()
        print "test [%s] used : %s" % (func.__name__, (end - start))
        return result
    return wrapper



