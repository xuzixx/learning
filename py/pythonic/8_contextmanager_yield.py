from contextlib import contextmanager
import pdb

@contextmanager
def test(x):
    try:
        yield x
    finally:
        print "finally exit"

#pdb.set_trace()
a = test(123)
print "[1] %s" % a
print "[2] %s" % type(a)

with test(123) as b:
    print "[3] %s" % b
    print "[4] %s" % type(b)

print "--- over"
"""
session 应用，finally close
output : 
    [1] <contextlib.GeneratorContextManager object at 0x103b22a90>
    [2] <class 'contextlib.GeneratorContextManager'>
    [3] 123
    [4] <type 'int'>
    finally exit
    --- over
"""
