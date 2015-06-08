#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import datetime
from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add = True)
    update_time = models.DateTimeField('更新时间', auto_now = True)

    def __unicode__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)
    
    class Meta:
        abstract = True
