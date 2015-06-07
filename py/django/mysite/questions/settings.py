#!/usr/bin/python
#-*- Encoding: utf-8 -*-

import os, inspect

# 获取APP所在的绝对路径，一开始想要这样让每个APP自己有uploads目录
# 目前此设置没用
APP_BASE_DIR = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))

APP_UPLOAD_DIR = os.path.join(APP_BASE_DIR, "uploads")
