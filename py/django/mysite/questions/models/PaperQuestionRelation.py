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
    user_answer = models.CharField("答案", max_length = 500, blank = True, default = "")
    score = models.IntegerField("得分", default = -1) # -1 表示此题目还没有做

    def arround_question(self):
        """
            依赖 每个paper中seq_num都是递增，不可重复的
            return : (前一道题, 后一道题)
        """
        next_pqrs = PaperQuestionRelation.objects.filter(seq_num = self.seq_num + 1).filter(paper__id = self.paper.id)
        prev_pqrs = PaperQuestionRelation.objects.filter(seq_num = self.seq_num - 1).filter(paper__id = self.paper.id)
        n = next_pqrs[0] if next_pqrs else None
        p = prev_pqrs[0] if prev_pqrs else None
        return (p, n)
        
    def __unicode__(self):
        return "<PaperQuestionRelation: %s, %s>" % (self.paper.id, self.question.id)
