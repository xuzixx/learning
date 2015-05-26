#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Question, Choice

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
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {'question' : question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question' : p, "error_message":"you didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # args = (p.id) # 这样会报错
        return HttpResponseRedirect(reverse('polls:results', args = (p.id,)))

""" ---------- Use generic views --------- 
    Writing your first Django app, part 4
"""
from django.views import generic
class IndexView(generic.ListView):
    template_name = 'polls/question_list.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    # By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html. 
    # Similarly, the ListView generic view uses a default template called <app name>/<model name>_list.html; 
    # 所以注释掉 也会去找这个模板
    #template_name = 'polls/question_detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/question_results.html'

""" def vote 用的还是之前的方法，所以跳转不到polls_generic """



