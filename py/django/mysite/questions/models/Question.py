#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *

Q_TYPE_SIZES = (
    ("SC" , "单选题"),
    ("MC" , "多选题"),
    ("SA" , "简答题"),
)

class Question(BaseModel):
    type = models.CharField("题目类型", max_length = 5, choices = Q_TYPE_SIZES) # q.get_type_display()
    title = models.CharField('题目标题', max_length = 250)
    problem = models.TextField("题目", default = "")
    answer = models.CharField("答案", max_length = 250, default = "")

    def __unicode__(self):
        return "<Question: %s>" % self.title

