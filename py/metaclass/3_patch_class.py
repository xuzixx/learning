#!/usr/bin/python
#coding:utf-8 


def monkey_patch(name, bases, dct):
    print name
    print bases
    print dct
    assert len(bases) == 1
    base = bases[0]
    for name, value in dct.iteritems():
        if name not in ('__module__','__metaclass__'):
            setattr(base, name, value)
    return base

class A(object):
    def a(self):
        print "i am A object"

class PatchA(A):
    __metaclass__ = monkey_patch

    def patcha_method(self):
        print 'this is a method patched for class A'

class InheritA(A):
    def inherita_method(self):
        print "this is a inherit "
        

def main():
    """ 3. 当引入第三方库的时候，如果该库某些类需要patch的时候可以用metaclass
    A, PatchA, InheritA 都有patcha_method """
    print "-----main"
    print dir(A)
    print dir(PatchA)
    print dir(InheritA)
    #pa = PatchA()
    #pa.patcha_method()
    #pa.a()
    #print dir(pa)
    #ia = InheritA()
    #ia.inherita_method()
    #ia.a() 
    #print dir(ia)

if __name__ == '__main__':
    main()
