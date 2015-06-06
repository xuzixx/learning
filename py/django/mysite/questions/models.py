#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

class QuestionUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("用户名", max_length = 50) 
    email = models.EmailField("邮箱")
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    update_time = models.DateTimeField('更新时间', auto_now = True)

    def __unicode__(self):
        return "<QuestionUser: %s, %s>" % (self.id, self.name)

class Question(models.Model):
    Q_TYPE_SIZES = (
        ("SC" , "单选题"),
        ("MC" , "多选题"),
        ("SA" , "简答题"),
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField("题目类型", max_length = 5, choices = Q_TYPE_SIZES) # q.get_type_display()
    title = models.CharField('题目标题', max_length = 250)
    problem = models.TextField("题目", default = "")
    answer = models.CharField("答案", max_length = 250, default = "")
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    update_time = models.DateTimeField('更新时间', auto_now = True)

    def __unicode__(self):
        return "<Question: %s>" % self.title

class Paper(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField("试卷标题", max_length = 250, default = "TEST (%s)" % datetime.date.today())
    questions = models.ManyToManyField(Question, 
        through = 'PaperQuestionRelation',
        through_fields = ('paper', 'question'), # tuple元素顺序重要
        related_name = 'papers' # tips 1
    )
    user = models.ForeignKey(QuestionUser, 
        related_name = "papers",
        related_query_name = "paper", # tips 2
    )
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    update_time = models.DateTimeField('更新时间', auto_now = True)
    
    def __unicode__(self):
        return "<Paper: %s, %s>" % (self.user.name, self.id)

class PaperQuestionRelation(models.Model):
    paper = models.ForeignKey(Paper, related_name = "question_relations")
    question = models.ForeignKey(Question, related_name = 'paper_relations')
    seq_num = models.IntegerField("题目序号")
    user_answer = models.CharField("答案", max_length = 500)
    score = models.IntegerField("得分")
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    update_time = models.DateTimeField('更新时间', auto_now = True)

    def __unicode__(self):
        return "<PaperQuestionRelation: %s, %s>" % (self.paper.id, self.question.id)

