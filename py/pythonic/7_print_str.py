#!/usr/bin/python
#-*- Encoding: utf-8 -*-


def print_s_r():
    """
    hello   World

    'hello\tWorld\n'
    """
    string = "hello\tWorld\n"
    print "%s" % string
    print "%r" % string

def print_number():
    """
    100 to hex is 64
    100 to hex is 64
    100 to hex is 0x64
    100 to hex is 0X64
    1.000000e+02
    value of f is: 3.1416
    =======================================================
    %d / %i | 转成有符号十进制数
    %u      | 转成无符号十进制数
    %x / %X | 转成无符号十六进制数（x / X 代表转换后的十六进制字符的大小写）
    %e / %E | 转成科学计数法（e / E控制输出e / E）
    %f / %F | 转成浮点数（小数部分自然截断）
    %%      | 输出% （格式化字符串里面包括百分号，那么必须使用%%）
    =======================================================
    """
    num = 100
    print "%d to hex is %x" % (num, num)
    print "%d to hex is %X" % (num, num)
    print "%d to hex is %#x" % (num, num)
    print "%d to hex is %#X" % (num, num) 
    print "%e" % num

    f = 3.1415926
    print "value of f is: %.4f" %f

def print_align():
    """
    name:     Wilber, age:         27
    name: Will      , age: 28
    name:       June, age: 0000000027
    Wilber is 27 years old
    Will is 28 years old
    June is 27 years old
    =======================================================
    *       | 定义宽度或者小数点精度
    -       | 用做左对齐
    +       | 在正数前面显示加号(+)
    #       | 在八进制数前面显示零(0)，
            | 在十六进制前面显示"0x"或者"0X"（取决于用的是"x"还是"X"）
    0       | 显示的数字前面填充"0"而不是默认的空格
    (var)   | 映射变量（通常用来处理字段类型的参数）
    m.n     | m 是显示的最小总宽度，n 是小数点后的位数（如果可用的话）
    =======================================================
    """
    # 指定宽度和对齐
    students = [
        {"name":"Wilber", "age":27}, 
        {"name":"Will", "age":28}, 
        {"name":"June", "age":27}]
    print "name: %10s, age: %10d" % (students[0]["name"], students[0]["age"])
    print "name: %-10s, age: %-10d" % (students[1]["name"], students[1]["age"])
    print "name: %*s, age: %0*d" % (10, students[2]["name"], 10, students[2]["age"])
    # dict参数
    for student in students:
        print "%(name)s is %(age)d years old" % student

def str_func():
    """
    str 内建函数

    abcdefg
    ABCDEFG
    AbCdEfG
    Abcdefg
    --- 输出width个字符，S左对齐，不足部分用fillchar填充，默认的为空格
    aBcDeFg***
    ---aBcDeFg
    ~aBcDeFg~~
     aBcDeFg
     --- find/count/replace
     abcdeeeee
     3
     8
     5
     abcdffeee
    """
    s = "aBcDeFg"
    print s.lower()
    print s.upper()
    print s.swapcase()
    print s.capitalize()
    print "--- 输出width个字符，S左对齐，不足部分用fillchar填充，默认的为空格"
    print s.ljust(10, '*')
    print s.rjust(10, '-')
    print s.center(10, '~')
    print s.center(10)
    s2 = "abcdeeeee"
    print "--- find/count/replace"
    print s2
    print s2.find("de", 0 , 100)
    print s2.rfind("e")
    print s2.count('e')
    x = s2.replace('e', 'f', 2)
    print x
    
if __name__ == "__main__":
    #print_s_r()
    #print_number()
    #print_align()
    str_func()
