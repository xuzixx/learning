#!/usr/bin/python
#coding:utf-8 

from types import FunctionType 

def login_required(func):
    print 'login check logic here'
    return func

class LoginDecorator(type): 
    def __new__(cls, name, bases, dct):
        for name, value in dct.iteritems():
            if name not in ('__metaclass__', '__init__', '__module__') and\
                type(value) == FunctionType:
                value = login_required(value)
                
            dct[name] = value
        return type.__new__(cls, name, bases, dct)

class Operation(object):  
    __metaclass__ = LoginDecorator  
    def delete(self, x): 
        print 'deleted %s' % str(x)  

def main():
    """
    2、批量的对某些方法使用decorator，而不需要每次都在方法的上面加入@decorator_func
    给 Operation 的实例的所有方法 都添加过滤
    可以不用在delete函数上面写@login_required, 也能达到decorator的效果了。不过可读性就差点了。
    """
    op = Operation()  
    op.delete('test')

if __name__ == '__main__': 
    main()
