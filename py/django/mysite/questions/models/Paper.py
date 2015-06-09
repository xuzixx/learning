#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *
from Question import *
from PaperUser import *

P_STATUS_SIZE = (
    ('DOING','正在答题'),
    ('GRADING','简答题待评分'),
    ('DONE','已答完'),
    ('CANCAL','作废'),
)

P_TYPE_SIZES = (
    ("ALL" , "默认全部"),
    ("RANDOM" , "随机出题"),
)
class PaperTemplate(BaseModel):
    title = models.CharField(u"试卷模板标题", max_length = 250, default = "TEMPLATE (%s)" % datetime.date.today())
    questions = models.ManyToManyField(Question, 
        related_name = 'paper_templates'
    )
    #questions = models.ManyToManyField(Question)
    type = models.CharField(u"出题方式", max_length = 10, choices = P_TYPE_SIZES, default = "ALL")
    conf_sc = models.IntegerField(u"单选题随机数目", default = 0)
    conf_mc = models.IntegerField(u"多选题随机数目", default = 0)
    conf_sa = models.IntegerField(u"简答题随机数目", default = 0)
    
    def __unicode__(self):
        return "<Paper: %s>" % self.title


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
    status = models.CharField("试卷状态", max_length = 10, choices = P_STATUS_SIZE, default = "DOING") 
    template = models.ForeignKey(PaperTemplate, related_name = "papers", null = True, blank = True)
    
    def __unicode__(self):
        return "<Paper: %s, %s>" % (self.user.name, self.title)
        



