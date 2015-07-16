#!/usr/bin/python
#-*- Encoding: utf-8 -*-

def foo(a, b, c = []):
    c.append(a)
    c.append(b)
    print c

def betterfoo(a, b, c = None):
    if c is None:
        c = []
    c.append(a)
    c.append(b)
    print c

if __name__ == '__main__':
    foo(1, 2)
    #[1, 2]
    foo(3, 4)
    #[1, 2, 3, 4] !!!
    foo(5, 6, c = [0])
    #[0, 5, 6]
