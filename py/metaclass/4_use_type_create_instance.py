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
    """ 利用type 动态生成     
    type(name, bases, dict) 
        The name string is the class name and becomes the __name__ attribute;
        the bases tuple itemizes the base classes and becomes the __bases__ attribute;
        the dict dictionary is the namespace containing definitions for class body and becomes the __dict__ attribute.
    """
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

    """
    Myclass ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    TypeCreateClassA ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    TypeCreateClassB ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    TypeCreateClassC ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'add_method']
    --- type new instance
    Base init
    MyClass init 1
    MyClass init 2
    TypeCreateClassA <__main__.MyClass object at 0x10c1c0250>
    TypeCreateClassB <__main__.MyClass object at 0x10c1c0290>
    TypeCreateClassC <__main__.MyClass object at 0x10c1c02d0>
    --- init new instance
    MyClass init 4
    <__main__.MyClass object at 0x10c1c0310>
    """
