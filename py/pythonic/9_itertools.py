#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import unittest
from itertools import *

class TestItertools(unittest.TestCase):

    def test_groupby(self):
        print "---- test_groupby"
        def _get_key(item):
            """
                return: groupby的key
            """
            a = item.split(',')
            key = a[0]
            return key

        def _split(iter):
            for i in iter:
                url, v1, v2 = i.split(',')
                yield v1, v2

        groupby_list = [
            "url1,1,10",
            "url1,2,20",
            "url2,3,30",
            "url2,4,40",
            "url3,5,50",
        ]
        print "---- vs"
        for k, vs in groupby(groupby_list, _get_key):
            print k, list(vs)

        print "---- split"
        for k, vs in groupby(groupby_list, _get_key):
            v1_sum = 0
            v2_sum = 0
            for v1, v2 in _split(vs):
                v1_sum += int(v1)
                v2_sum += int(v2)
            print k, v1_sum, v2_sum


if __name__ == "__main__":
    unittest.main()




