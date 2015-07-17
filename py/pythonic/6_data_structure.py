#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from collections import namedtuple
"""
    namedtuple 命名元组 
    下面三个方法 namedtuple 第二个参数略有区别
"""
def collections_namedtuple_test():
    """
    result:
        1 Type of Person: <type 'type'>
        2 Representation: Person(name='Bob', age=30, gender='male')
        3 <class '__main__.Person'>
        4 Field by Name: Bob
        ---------------------
        ('name', 'age', '_2', 'gender')
        ('name', 'age', 'gender', '_3')
    """
    Person = namedtuple('Person', 'name age gender')
    print '1 Type of Person:', type(Person)
    Bob = Person(name='Bob', age=30, gender='male')
    print '2 Representation:', Bob
    print "3", type(Bob)
    print '4 Field by Name:', Bob.name
    print '--------------------'
    with_class = namedtuple('Person', 'name age class gender', rename=True)
    two_ages = namedtuple('Person', 'name age gender age', rename=True)
    print with_class._fields
    print two_ages._fields
    """
    tips:
        但是在使用namedtuple的时候要注意其中的名称不能使用Python的关键字，如：class def等；
        而且也不能有重复的元素名称，比如：不能有两个’age age’。如果出现这些情况，程序会报错。
        但是，在实际使用的时候可能无法避免这种情况，
        比如:可能我们的元素名称是从数据库里读出来的记录，这样很难保证一定不会出现Python关键字。
        这种情况下的解决办法是将namedtuple的重命名模式打开，
        这样如果遇到Python关键字或者有重复元素名时，自动进行重命名。
    """

def basic_test():
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(11, y = 22)
    print 'indexable like the plain tuple (11, 22)'
    print p[0]
    print p[1]
    print 'field also accessible by name'
    print p.x
    print p.y
    print p

def csv_sqlite_example():
    EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department')
    import csv
    for emp in map(EmployeeRecord._make, csv.reader(open('employees.csv', 'rb'))):
        print (emp.name, emp.title)
    import sqlite3
    con = sqlite3.connect('/companydata')
    cursor = con.cursor()
    cursor.execute('select name, age, title, department from employees')
    for emp in map(EmployeeRecord._make, cursor.fetchall()):
        print (emp.name, emp.title)

if __name__ == "__main__":
    collections_namedtuple_test()
    print '=' * 40
    basic_test()
    print '=' * 40
