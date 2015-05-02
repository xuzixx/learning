#!/usr/bin/python
#coding:utf-8 

class MyBase(object):
    def __init__(self):
        print "Base init"

class MyClass(MyBase):
    def __init__(self, msg):
        print "MyClass init %s" % msg

if __name__ == '__main__':
    """ 利用type 动态生成 """
    TypeCreateClass = type('MyClass',(MyBase,),{})
    print TypeCreateClass
    print dir(TypeCreateClass)
    print dir(MyClass)
    print "--- type new instance"
    instance = TypeCreateClass()
    print instance
    print "--- init new instance"
    mi = MyClass(4)
    print mi
