#!/usr/bin/python
#coding:utf-8 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

""" 你可以自由的、动态的修改/增加/删除 类的或者实例中的方法或者属性 """
def ma(cls):
    print "method a"

def mb(cls):
    print "method b"

method_dict = {
    'ma' : ma,
    'mb' : mb,
}

class DynamicMethod(type):
    def __new__(cls, name, bases, dct):
        """
        cls: 将要创建的类，类似与self，但是self指向的是instance，而这里cls指向的是class
        name: 类的名字，也就是我们通常用类名.__name__获取的。
        bases: 基类
        attrs: 属性的dict。dict的内容可以是变量(类属性），也可以是函数（类方法）。
        """
        if name[:3] == 'Abc':
            dct.update(method_dict)
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(DynamicMethod, cls).__init__(name, bases, dct)

class AbcTest(object):
    __metaclass__ = DynamicMethod
    def mc(self, x):
        print x * 3

class NotAbc(object):
    __metaclass__ = DynamicMethod
    def md(self, x):
        print x * 3

def main():
    """
    1. 你可以自由的、动态的修改/增加/删除 类的或者实例中的方法或者属性
    通过DynamicMethod这个metaclass的原型，我们可以在那些指定了__metaclass__属性位DynamicMethod的类里面，
    根据类名字，如果是以'Abc'开头的就给它加上ma和mb的方法(这里的条件只是一种简单的例子假设了，实际应用上
    可能更复杂）,如果不是'Abc'开头的类就不加. 这样就可以打到动态添加方法的效果了。其实，你也可以将需要动态
    添加或者修改的方法改到__new__里面，因为python是支持在方法里面再定义方法的. 通过这个例子，其实可以看到
    只要我们能操作__new__方法里面的其中一个参数attrs，就可以动态添加东西了。
    """
    global method_dict
    print method_dict
    a = AbcTest()
    a.mc(3)
    a.ma()
    print "[instance a] %s" % dir(a)
    """ 全局修改了method_dict 也不会使instance c方法改变 """
    method_dict = {'me':ma}
    print "[instance a] %s" % dir(a)
    c = AbcTest()
    print "[instance c] %s" % dir(c)
    b = NotAbc()
    print "[instance b] %s" % dir(b)

if __name__ == '__main__':
    main()

