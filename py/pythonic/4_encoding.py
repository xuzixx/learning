#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import chardet
from chardet.universaldetector import UniversalDetector  
import urllib

"""
    安装包后系统自带命令:
    chardetect README.md
    README.md: utf-8 with confidence 0.99
"""

def simple_encoding_test():
    """ 01 简单探测编码应用 """
    data = urllib.urlopen("http://www.baidu.com").read()
    print chardet.detect(data)


def bigfile_encoding_test():
    """ 02 大文件探测编码应用 """
    usock = urllib.urlopen('http://www.baidu.com/')
    detector = UniversalDetector()
    for line in usock.readlines():
        #print line
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    usock.close()
    print detector.result

def coding_test():
    """ 03 原有编码 > 内部编码 > 目的编码 """
    a = "测试测试"
    print type(a) # <type 'str'>
    b = a.decode("utf-8")
    print type(b) # <type 'unicode'>
    # f = codecs.open(file_path, 'r', file_encoding, errors="ignore")


if __name__ == "__main__":
    print """ 01 简单探测编码应用 """
    # simple_encoding_test() # {'confidence': 0.99, 'encoding': 'utf-8'}
    print """ 02 大文件探测编码应用 """
    # bigfile_encoding_test() # {'confidence': 0.99, 'encoding': 'utf-8'}
    print """ 03 原有编码 > 内部编码 > 目的编码 """
    coding_test()

