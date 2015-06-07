#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *
from Question import *

class QuestionPic(BaseModel):
    question = models.ForeignKey(Question, related_name = "question_pics")
    # failed : 
    #pic = models.ImageField(upload_to = 'QuestionPic/%Y/%m/%d', storage = fs)
    pic = models.ImageField(upload_to = 'questions/QuestionPic/%Y/%m/%d', blank = True)

    def __unicode__(self):
        if self.pic:
            tag = self.pic.path
        else:
            tag = self.id
        return "<QuestionPic: %s>" % tag


