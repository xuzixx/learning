#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *
from Question import *
from Paper import *

class PaperQuestionRelation(BaseModel):
    paper = models.ForeignKey(Paper, related_name = "question_relations")
    question = models.ForeignKey(Question, related_name = 'paper_relations')
    seq_num = models.IntegerField("题目序号")
    user_answer = models.CharField("答案", max_length = 500)
    score = models.IntegerField("得分")

    def __unicode__(self):
        return "<PaperQuestionRelation: %s, %s>" % (self.paper.id, self.question.id)



