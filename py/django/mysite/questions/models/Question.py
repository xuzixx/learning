#!/usr/bin/python
#-*- Encoding: utf-8 -*-

from django.db import models
from django import forms

from BaseModel import *

Q_TYPE_SIZES = (
    ("SC" , "单选题"),
    ("MC" , "多选题"),
    ("SA" , "简答题"),
)

class Question(BaseModel):
    type = models.CharField("题目类型", max_length = 5, choices = Q_TYPE_SIZES) # q.get_type_display()
    title = models.CharField('题目标题', max_length = 250)
    problem = models.TextField("题目", default = "")
    answer = models.CharField("正确答案", max_length = 250, blank = True, default = "")
    
    def get_anserform(self, *data):
        queryset = self.answer_list.all()
        if self.type == "SC":
            return SCAnswerForm(*data, answer_list = queryset)
        elif self.type == "MC":
            return MCAnswerForm(*data, answer_list = queryset)
        elif self.type == "SA":
            return SAAnswerForm(*data)
        else:
            return None
    
    def check_answer(self, answer):
        if self.type == "SA":
            return True
        else:
            if set(answer) == set(self.answer):
                return True
            else:
                return False
    
    def __unicode__(self):
        return "<Question: %s>" % self.title

class QuestionAnswer(BaseModel):
    question = models.ForeignKey(Question, related_name = 'answer_list')
    key = models.CharField('答案选项', max_length = 1)
    content = models.CharField('候选答案内容', max_length = 250)
    
    def __unicode__(self):
        return "%s: %s" % (self.key, self.content)


class SCAnswerForm(forms.Form):
    answer = forms.ModelChoiceField(label='答案', 
        queryset=None, 
        empty_label=None, 
        to_field_name="key", 
        widget=forms.RadioSelect
    )  
    
    def __init__(self, *args, **kwargs):
        answer_list = kwargs["answer_list"]
        del kwargs["answer_list"]
        super(SCAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = answer_list
    
class MCAnswerForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(label='答案', queryset=None, to_field_name="key", widget=forms.CheckboxSelectMultiple)  
    
    def __init__(self, *args, **kwargs):
        answer_list = kwargs["answer_list"]
        del kwargs["answer_list"]
        super(MCAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = answer_list
    
class SAAnswerForm(forms.Form):
    answer = forms.CharField(label='答案', max_length = 500, widget=forms.Textarea)