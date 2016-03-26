#!/usr/bin/python
#-*- Encoding: utf-8 -*-

def test_type_object():
    """
    ---tuple
    <type 'type'>
    <type 'type'>
    (<type 'object'>,)
    ---list
    <type 'type'>
    <type 'type'>
    (<type 'object'>,)
    ---dict
    <type 'type'>
    <type 'type'>
    (<type 'object'>,)
    ---mylist
    <type 'list'>
    <type 'list'>
    """
    print "---tuple"
    print tuple.__class__
    print type(tuple)
    print tuple.__bases__
    print "---list"
    print list.__class__
    print type(list)
    print list.__bases__
    print "---dict"
    print dict.__class__
    print type(dict)
    print dict.__bases__
    print "---mylist"
    mylist = [1, 2, 3]
    print mylist.__class__
    print type(mylist)

def test_id_compare():
    """
    obj1 is obj2
    # 等价
    id(obj1) == id(obj2)
    """
    pass
    
def test_type_compare():
    """
    True
    True
    True
    True
    ----A
    <type 'type'>
    True
    True
    True
    ----a
    <class '__main__.A'>
    True
    True
    True
    """
    import types
    print type(1) == types.IntType
    print type(1) is types.IntType
    print isinstance(1, types.IntType)
    print isinstance(1, int)
    print "----A"
    class A(object):
        pass
    print type(A)
    print type(A) == types.TypeType
    print type(A) is types.TypeType
    print isinstance(A, types.TypeType)
    print "----a"
    a = A()
    print type(a)
    print type(a) == A
    print type(a) is A
    print isinstance(a, A)

def test_int_cache():
    """
    c 超出了Python 对整型的缓存范围
    True
    True
    --- out of range
    False
    True
    """
    a = 3
    b = 2 + 1
    print a is b
    print a == b
    print "--- out of range"
    c = 10000000000 + 1
    d = 10000000001
    print c is d
    print c == d

def test_mutable_immutable():
    """
    不可变（immutable）对象：对象的内容不可变，当尝试改变对象内容的时候，会创建一个新的对象；也就是说对象的身份（id()）会发生变化
    例如：number、string，tuple

    可变（mutable）对象：对象的内容可变，当改变对象内容的时候，对象的身份（id()）不会变化
    例如：list、dict、set

    4487928592
    4487928640
    !!! --- tuple
    4487846400
    4487785648
    !!! --- list
    4487715368
    4487715368
    --- antihuman
    (1, 2, 3, [4, 5, 6])
    4487866512
    4487817840
    --- extend
    4487817840
    (1, 2, 3, [4, 5, 6, 7, 8])
    4487866512
    """
    s = "Hello"
    print id(s)
    s = "World"
    print id(s)
    print "!!! --- tuple"
    tpl = (1, 2, 3)
    print id(tpl)
    tpl = (4, 5)
    print id(tpl)
    print "!!! --- list"
    l = [1, 2, 3]
    print id(l)
    l += [4, 5]
    print id(l)
    print "--- antihuman"
    tpl = (1, 2, 3, [4, 5, 6])
    print tpl
    print id(tpl)
    print id(tpl[3])
    print "--- extend"
    tpl[3].extend([7, 8])
    print id(tpl[3])
    print tpl
    print id(tpl)
    
if __name__ == "__main__":
        #test_type_object()
        #test_type_compare()
        #test_int_cache()
        test_mutable_immutable()




