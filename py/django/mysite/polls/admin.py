#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """ 
        两种展现形式
        admin.TabularInline
        admin.StackedInline
    """
    fields = ["votes", "choice_text"] # 依然可以排序
    model = Choice
    extra = 3 # 默认给3个choice 框体

class QuestionAdmin(admin.ModelAdmin):
    # 影响admin界面中字段出现顺序
    #fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently') # Questions 列表显示字段(默认只是 str/unicode 显示的内容)
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (
            "Date information/日期信息", 
            # fields : 字段, classes : show/hidden 切换
            {'fields': ['pub_date'], 'classes': ['collapse']}
        ),
    ]
    list_filter = ['pub_date'] # admin界面添加快捷的过滤条件
    search_fields = ['question_text'] # admin界面添加搜索
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

