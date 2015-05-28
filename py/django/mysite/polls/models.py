#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        """ 
        __str__ or __unicode__?

        On Python 3, it’s easy, just use __str__().

        On Python 2, you should define __unicode__() methods returning unicode values instead. Django models have a default __str__() method that calls __unicode__() and converts the result to a UTF-8 bytestring. This means that unicode(p) will return a Unicode string, and str(p) will return a bytestring, with characters encoded as UTF-8. Python does the opposite: object has a __unicode__ method that calls __str__ and interprets the result as an ASCII bytestring. This difference can create confusion.

        If all of this is gibberish to you, just use Python 3.
        """
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(minutes = 5)

    # 为了admin 界面后台显示 tips [Writing your first Django app, part 2]
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "最近发布?"

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.choice_text
