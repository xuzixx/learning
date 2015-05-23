#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import fileinput
import glob

#处理一个文本文件  
for line in fileinput.input("README.md"):       
    #获得当前文件名称  
    print fileinput.filename()  
    #获得当前行编号（在多文件中，所有文件中的行数。即遇到新文件不重新计数）  
    print fileinput.lineno()  
    #获得当前行编号 （当前行在所在文件的行数）  
    print fileinput.filelineno()  
    #当前行是否是当前文件的首行  
    print fileinput.isfirstline()  



#处理多个文本文件  
for line in fileinput.input(glob.glob("*.py")):   
    print line.strip()
