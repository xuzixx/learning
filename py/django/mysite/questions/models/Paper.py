#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *
from Question import *
from PaperUser import *


class Paper(BaseModel):
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
    
    def __unicode__(self):
        return "<Paper: %s, %s>" % (self.user.name, self.id)



