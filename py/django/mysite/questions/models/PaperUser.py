#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models

from BaseModel import *

class PaperUser(BaseModel):
    name = models.CharField("用户名", max_length = 50) 
    email = models.EmailField("邮箱")

    def __unicode__(self):
        return "<PaperUser: %s, %s>" % (self.id, self.name)


