#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.contrib import admin

from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['type']
    search_fields = ['content']
    list_display = ['id','type','content','create_time','update_time']

class PaperQuestionsInline(admin.TabularInline):
    fields = ['seq_num','user_answer', 'score', 'question']
    model = PaperQuestionRelation
    extra = 0

class PaperAdmin(admin.ModelAdmin):
    list_display = ["user", 'title', 'create_time', 'update_time']
    fields = ['user', 'title']
    inlines = [PaperQuestionsInline]

class QuestionUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'create_time', 'update_time']
    fields = ['name', 'email']
#    fieldsets = [
#        (None, {'fields': ['name', 'email']}),
#        ("日期信息", {
#            'fields': ['create_time', "update_time"],
#            'classes': ['collapse']
#        })
#    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(QuestionUser, QuestionUserAdmin)
