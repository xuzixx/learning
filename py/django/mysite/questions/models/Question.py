#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from collections import Iterable

from django.db import models
from django import forms

from BaseModel import *

Q_TYPE_SIZES = (
    ("01SC" , u"单选题"),
    ("02MC" , u"多选题"),
    ("03SA" , u"简答题"),
)

class Question(BaseModel):
    type = models.CharField(u"题目类型", max_length = 5, choices = Q_TYPE_SIZES) # q.get_type_display()
    title = models.CharField(u'题目标题', max_length = 250)
    problem = models.TextField(u"题目", default = "")
    answer = models.CharField(u"正确答案", max_length = 250, blank = True, default = "")
    score = models.IntegerField(u"此题答对得分", default = 10)
    
    def get_answerform(self, *data):
        queryset = self.answer_list.all()
        if self.type == "01SC":
            return SCAnswerForm(*data, answer_list = queryset)
        elif self.type == "02MC":
            return MCAnswerForm(*data, answer_list = queryset)
        elif self.type == "03SA":
            return SAAnswerForm(*data)
        else:
            return None
    
    def check_answer(self, user_answers):
        """ 
            核对答案是否正确
            user_answers : 单选题： QuestionAnswer /多选题：[QuestionAnswer]/简答题：str
            return : (score, answer) score: 得分，answer: 答案字符串
        """
        if self.type == "03SA":
            return (0, user_answers)
        else:
            if isinstance(user_answers, Iterable):
                answer = "".join([qa.key for qa in user_answers])
            else:
                answer = user_answers.key
            if set(answer) == set(self.answer):
                return (self.score, answer)
            else:
                return (0, answer)
    
    def __unicode__(self):
        return "<Question: %s, %s>" % (self.title, self.get_type_display())

class QuestionAnswer(BaseModel):
    question = models.ForeignKey(Question, related_name = 'answer_list')
    key = models.CharField('答案选项', max_length = 1, help_text = "选项序号,如'A','B','C'")
    content = models.CharField('候选答案内容', max_length = 250)
    
    def __unicode__(self):
        return "%s: %s" % (self.key, self.content)


class SCAnswerForm(forms.Form):
    answer = forms.ModelChoiceField(
        label='答案', 
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
    answer = forms.ModelMultipleChoiceField(
        label='答案', 
        queryset=None, 
        to_field_name="key", 
        widget=forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        answer_list = kwargs["answer_list"]
        del kwargs["answer_list"]
        super(MCAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = answer_list
    
class SAAnswerForm(forms.Form):
    answer = forms.CharField(label='答案', max_length = 500, widget=forms.Textarea)

