#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.contrib import admin

from .models import *

class QuestionPicInline(admin.StackedInline):
    model = QuestionPic
    extra = 0

class QuestionAnswerInline(admin.TabularInline):
    fields = ["key", "content"]
    model = QuestionAnswer
    extra = 0
    
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['type']
    search_fields = ['title']
    list_display = ['id','type','title','answer','create_time','update_time']
    inlines = [QuestionAnswerInline, QuestionPicInline]

class PaperQuestionsInline(admin.TabularInline):
    fields = ['seq_num','user_answer', 'score', 'question']
    model = PaperQuestionRelation
    extra = 0
    
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id',"user", 'title', 'status', 'create_time', 'update_time']
    fields = ['user', 'title', 'status', 'template']
    inlines = [PaperQuestionsInline]

class PaperTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'create_time', 'update_time']
    fields = ['title', 'type', 'conf_sc', 'conf_mc', 'conf_sa', 'questions']
    #inlines = [QuestionInline]
    filter_vertical = ('questions',)
    
class PaperUserAdmin(admin.ModelAdmin):
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
admin.site.register(PaperUser, PaperUserAdmin)
admin.site.register(PaperTemplate, PaperTemplateAdmin)
