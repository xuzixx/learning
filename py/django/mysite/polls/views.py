#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Question

def hello_world(request):
    return HttpResponse("Hello world,index")

def index_old_v1(request):
    """ 
        可以用 render 简化
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list' : latest_question_list,
    })
    return HttpResponse(template.render(context))

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

def detail_old_v1(request, question_id):
    """
        可以用 get_object_or_404 简化
    """
    try:
        question = Question.objects.get(pk = question_id)
    except:
        raise Http404("question does not exist")
    return render(request, 'polls/detail.html', {"question" : question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {"question" : question})


def results(request, question_id):
    response = "you are looking at the results of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("you are voting on question %s" % question_id)






