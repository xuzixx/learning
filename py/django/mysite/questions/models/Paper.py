#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *
from Question import *
from PaperUser import *

P_STATUS_SIZE = (
    ('DOING','正在答题'),
    ('GRADING','待评分'),
    ('DONE','已答完'),
    ('CANCAL','作废'),
)

class Paper(BaseModel):
    # todo 自己是自己的father
    title = models.CharField("试卷标题", max_length = 250, default = "TEST (%s)" % datetime.date.today())
    questions = models.ManyToManyField(Question, 
        through = 'PaperQuestionRelation',
        through_fields = ('paper', 'question'), # tuple元素顺序重要
        related_name = 'papers' # tips 1
    )
    user = models.ForeignKey(PaperUser, 
        related_name = "papers",
        related_query_name = "paper", # tips 2
    )
    status = models.CharField("试卷状态", max_length = 10, choices = P_STATUS_SIZE, default = "DOING") 
    
    def __unicode__(self):
        return "<Paper: %s, %s>" % (self.user.name, self.id)



