#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.shortcuts import render, render_to_response

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from .models import *

def paper_new(request):
    """ 用户新创建一个paper """
    pass

def paper_index(request):
    """ 
        根据用户, 显示所有的paper 
        url : ^paper/$
    """
    # todo 权限
    paper_list = Paper.objects.filter(user__id = 1).order_by("-update_time")
    paginator = Paginator(paper_list,10)

    page = request.GET.get('page', 1)
    try:
        papers = paginator.page(page)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)
    return render_to_response('questions/paper_index.html', {'papers': papers})

def paper_detail(request, paper_id):
    """ 
        根据paper号 显示所有的questions 
        url : ^paper/(?P<paper_id>[0-9]+)/$
    """
    #question_list = Question.objects.filter(paper_relations__id = paper_id)
    pqr_list = PaperQuestionRelation.objects.filter(paper__id = paper_id).order_by("seq_num")
    # !!! pqrs 不是 questions
    return render_to_response('questions/question_list.html', {'pqrs': pqr_list})

def paper_result(request, paper_id):
    return HttpResponse(paper_id)

def user_submit(request, pqr_id):
    #user_answer = request.POST.get('user_answer', "")
    #pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    
    return render_to_response("questions/markdown_test.html", {})
   
@csrf_protect   
def question_detail(request, pqr_id):
    """ 
        显示具体question内容 
        url : ^question/(?P<pqr_id>[0-9]+)/$
    """
    pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    if request.method == 'POST':
        form = pqr.question.get_anserform(request.POST)
        print "=" * 50
        if form.is_valid():
            answer = form.cleaned_data['answer']
#            print form.cleaned_data
#            print answer
#        print "-" * 25
#        print request.POST
#        print "-" * 25
#        print form
#        print "=" * 50
        return HttpResponse(pqr.question.check_answer(answer))
    else:
        form = pqr.question.get_anserform()
        
    import markdown2
    return render(request, 'questions/question_detail.html', 
        {
            'pqr': pqr, 
            'form': form,
            "question_content": markdown2.markdown(pqr.question.problem)
        }
    )
    
def question_result(request, pqr_id):
    """ 
        显示具体question答案 
        url : ^question/(?P<pqr_id>[0-9]+)/result/$
    """
    import markdown2
    pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    return render_to_response('questions/question_result.html', 
            {'pqr': pqr, "question_content": markdown2.markdown(pqr.question.problem)}
        )


# -------------------------------- 
def test_question_detail(request, pqr_id):
    """ 
       question_detail 测试，不同方式实现 CSRF # tips
    """
    import markdown2
    pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    return render_to_response('questions/question_detail.html', 
            {'pqr': pqr, "question_content": markdown2.markdown(pqr.question.problem)},
            context_instance=RequestContext(request)
        )
        
def test_markdown(request):
    import markdown2
    q = Question.objects.get(pk = 1)
    print q.problem
    return render_to_response('questions/markdown_test.html', 
            {"my_content": markdown2.markdown(q.problem)}
        )

def test(request):
    return HttpResponse("hello")


