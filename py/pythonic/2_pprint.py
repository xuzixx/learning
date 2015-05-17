#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import pprint

""" 
    refer:
    http://blog.csdn.net/iamaiearner/article/details/9378093
"""
a = {'a':1,'b':2,'c':3,"list_a" : ["123456789",2,3,4,{"d_2":123}]}

#
# pprint.pformat(object,indent=1,width=80, depth=None) 
# pprint.pprint(object,stream=None,indent=1, width=80, depth=None) 
pprint.pprint(a, indent = 4, width = 10, depth = 2)

# 漂亮的将文件中的json文档打印出来，你可以用以下这种方式：
# cat file.json |python -m json.tool

"""
{   'a': 1,
    'b': 2,
    'c': 3,
    'list_a': [   '123456789',
                  2,
                  3,
                  4,
                  {...}]}
"""


