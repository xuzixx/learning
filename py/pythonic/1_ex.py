#!/usr/bin/python
#-*- Encoding: utf-8 -*-

def list_to_dict():
    # 01 用两个元素之间有对应关系的list构造一个dict:
    names = ['jianpx', 'yue']  
    ages = [23, 40]  
    m = dict(zip(names,ages)) 
    print m
    """
        zip的使用可以help(zip)
        >>> a = [1,2]
        >>> b = [3,4]
        >>> zip(a,b)
        [(1, 3), (2, 4)]
        >>> help(zip)
        >>> c  = [5,6,7]
        >>> zip(a,b,c)
        [(1, 3, 5), (2, 4, 6)]
    """
    
def list_string_reverse():
    # 02 list, string 倒序
    a = [1, 2, 3, 4]
    b = "1234"
    aa = a[::-1]
    bb = b[::-1]
    print aa
    print bb

def enumerate_list():
    # 03 enumerate , 可以传递开始序号
    a = ['a', 'b', 'c', 'd']
    for i, item in enumerate(a):
        print i, item
    print '-' * 10
    for i, item in enumerate(a, 1):
        print i, item

if __name__ == "__main__":
    enumerate_list()
