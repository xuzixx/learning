#!/bin/env pyhon
#coding=utf-8
import os, sys
sys.path.append("..")
import time
import traceback
import zlib

from models import *
from tool import *

"""
在创建LogInfo实例过程中,创建的异常都是格式错误，记录exception_count
"""

@test_timer
def cmps_result(result_str):
    """ 压缩内存 """
    result_cmps = zlib.compress(result_str, zlib.Z_BEST_COMPRESSION)
    return result_cmps

@test_timer
def dcmps_result(result_cmps):
    """ 解压内存 """
    result_str = zlib.decompress(result_cmps)
    return result_str

def test_code_kinds(file_name = ""):
    """ 测试日志文件中有多少中 http_code """
    code_kinds = set()
    with open(file_name) as file:
        for line in file:
            try:
                log_info = LogInfo(line)
                code_kinds.add(log_info.status)
            except LogInfoException, e:
                pass
    return code_kinds

def main(file_name = "", deal_time = time.time(), result_dict = {}):
    """ 
        处理一个文件，得到结果集合，错误数，异常数
        return [result_dict, exception_count, warning_count] 
        result_dict : 
            key : url|http_code
            value : http_code counts
    """ 
    exception_count = 0
    warning_count = 0
    with open(file_name) as file:
        for line in file:
            try:
                log_info = LogInfo(line)
                # warning判断
                # 正常处理上一分钟的日志（09分处理08-09的日志）
                if deal_time - float(log_info.msec) > 60:
                    warning_count = warning_count + 1
                # refer根据规则修改,photocdn 用refer替换 url
                # 没有refer的用目录规则替换
                # 为什么要替换url？还是url + refer 不好吗？
                #if log_info.url in GLOBAL_RULE:
                #    self.

                #生成结果集
                key = log_info.get_error_code_key()
                if(result_dict.get(key)):
                    result_dict[key] = result_dict.get(key) + 1
                else:
                    result_dict[key] = 1

            except LogInfoException, e:
                exception_count = exception_count + 1
            except Exception, e:
                print line
                exception_count = exception_count + 1
                exstr = traceback.format_exc()
                print exstr
    #for i,key in enumerate(result_dict):
    #    print "[%s,%s] %s" %(i, key, result_dict[key]) 
    return [result_dict, exception_count, warning_count]

@test_timer
def test_main_size(file_name):
    result_dict = {}
    rlist = main(file_name = file_name, result_dict = result_dict)

    #print "---result_dict key size"
    #print len(result_dict.keys())
    #print "---result msg size"    
    #print sys.getsizeof(rlist[0])

    cmps = cmps_result(rlist[0].__str__())
    print "---compress str size"
    print sys.getsizeof(cmps)
    dcmps = dcmps_result(cmps)
    print "---decompress str size"
    print sys.getsizeof(dcmps)

    print "---错误数量"
    print rlist[1]
    print "---warning数量"
    print rlist[2]
    print "---done"
    

if __name__ == "__main__":
    file_name = "../../log/access.201503021500.log"
    # TEST:测试一共有多少种http code
    #print test_code_kinds(file_name = file_name)
    # TEST:测试main方法内存
    test_main_size(file_name)

    #rlist = main(file_name = file_name)

