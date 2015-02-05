#coding=utf-8
import datetime
import functools
import tornado.ioloop
print "----begin"
# 默认间隔1s
def loop_call(second = 1):
    print "---loop init"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            tornado.ioloop.IOLoop.instance().add_timeout(
                datetime.timedelta(milliseconds = second*1000),
                wrapper,
            )
        return wrapper

    return decorator


def loop_call2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(milliseconds = 1*1000),
            wrapper,
            *args,
            **kwargs
        )
    return wrapper


#    def _deco(content):
#        print "--in call"
#        ret = func(content)
#        return ret
#    return _deco

print "---@ begin"
#@loop_call(second = 2) ,这样就是 每隔2s, print_time1函数不带参数
#@loop_call() 
#def print_time1(): 
#    print "print_time1:%s" % datetime.datetime.now() 

@loop_call2
def print_time2(content):
    print "print_time2 -- %s : %s" % (content, datetime.datetime.now())

#print_time1()
print "--------"
print_time2("content")
#print_time2("content2")
#print_time2("content3333")

tornado.ioloop.IOLoop.instance().start()
