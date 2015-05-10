#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from pylab import *
import random
import datetime

dates = []
counts = []

# 生成上个月25 日 到本月 24日 的区间日期
today = datetime.date.today()
endday = today.replace(day = 24)

lastm = today.replace(day = 1) - datetime.timedelta(days = 1)
startday = lastm.replace(day = 25)

#dates = [startday + datetime.timedelta(days = i) for i in xrange((endday - startday).days + 1)]
# -------------------------------------------

for i in xrange((endday - startday).days + 1):
    dates.append(startday + datetime.timedelta(days = i))
    counts.append(int(random.random() * 100))

plot(dates, counts)
ylim(0, max(counts))
title("test pylab")
#show()
savefig("png/1_pylab.png")



