#!/usr/bin/python
#coding:utf-8 

def add_method(self):
    print "%s add method" % self.__class__

class MyBase(object):
    def __init__(self):
        print "Base init"

class MyClass(MyBase):
    def __init__(self, msg):
        print "MyClass init %s" % msg

if __name__ == '__main__':
    """ 利用type 动态生成 """
    TypeCreateClassA = type('MyClass',(MyBase,),{})
    TypeCreateClassB = type('MyClass',(MyClass,),{})
    TypeCreateClassC = type('MyClass',(MyClass,),{"add_method" : add_method})
    print "Myclass %s" % dir(MyClass)
    print "TypeCreateClassA %s" % dir(TypeCreateClassA)
    print "TypeCreateClassB %s" % dir(TypeCreateClassB)
    print "TypeCreateClassC %s" % dir(TypeCreateClassC)

    print "--- type new instance"
    a = TypeCreateClassA()
    b = TypeCreateClassB(1)
    c = TypeCreateClassC(2)
    print "TypeCreateClassA %s" % a
    print "TypeCreateClassB %s" % b
    print "TypeCreateClassC %s" % c

    print "--- init new instance"
    mi = MyClass(4)
    print mi
