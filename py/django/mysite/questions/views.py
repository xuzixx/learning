#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import random

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from .models import *

def get_random_queryset(queryset, count):
    """ 返回查询结果中 随机的几个 """
    result = []
    tmp_range = range(queryset.count())
    random.shuffle(tmp_range)
    for i in tmp_range[:count]:
        result.append(queryset[i])
    return result
    
def paper_new(request):
    """ 用户新创建一个paper """
    ptmpl_id = request.GET.get('ptmpl', 1)
    ptmpl = PaperTemplate.objects.get(pk = ptmpl_id)
    u = PaperUser.objects.get(pk = 1)
    p = Paper(user = u, title = ptmpl.title, status = "DOING", template = ptmpl)
    p.save()
    q_list = []
    if ptmpl.type == 'ALL':
        q_list = Question.objects.filter(paper_templates__id = ptmpl_id).order_by("type")
    elif ptmpl.type == "RANDOM":
        sc_q = Question.objects.filter(paper_templates__id = ptmpl_id).filter(type = "01SC")
        # 返回 单选结果集 中的 配置个数的题目
        q_list = q_list + get_random_queryset(sc_q, ptmpl.conf_sc)
        mc_q = Question.objects.filter(paper_templates__id = ptmpl_id).filter(type = "02MC")
        q_list = q_list + get_random_queryset(mc_q, ptmpl.conf_mc)
        sa_q = Question.objects.filter(paper_templates__id = ptmpl_id).filter(type = "03SA")
        q_list = q_list + get_random_queryset(sa_q, ptmpl.conf_sa)
    # 生产
    pqr_list = []
    for i, q in enumerate(q_list, 1):
        pqr_list.append(PaperQuestionRelation(paper = p, question = q, seq_num = i))
    PaperQuestionRelation.objects.bulk_create(pqr_list)
    #return HttpResponse("paper %s" % p.id)
    return redirect('questions:paper_detail', p.id)

def paper_index(request):
    """ 
        根据用户, 显示所有的paper 
        url : ^paper/$
    """
    paper_templates = PaperTemplate.objects.all()
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
    return render_to_response('questions/paper_index.html', {'papers': papers, "paper_templates": paper_templates})
    
@csrf_protect
def paper_detail(request, paper_id):
    """ 
        根据paper号 显示所有的questions 
        url : ^paper/(?P<paper_id>[0-9]+)/$
    """
    #question_list = Question.objects.filter(paper_relations__id = paper_id)
    pqr_list = PaperQuestionRelation.objects.filter(paper__id = paper_id).order_by("seq_num")
    if request.method == 'POST':
        # post 交卷操作
        # 未作答的题目也更新为0分
        pqr_list.filter(score = -1).update(score = 0)
        paper = Paper.objects.get(pk = paper_id)
        sa_questions = Question.objects.filter(papers__id = paper_id).filter(type = '03SA')
        if sa_questions:
            # 存在简答题，更改为 批改中 状态
            paper.status = "GRADING"
        else:
            paper.status = "DONE"
        paper.save()
        
        return render(request, 'questions/question_list.html', 
            {'pqrs': pqr_list, 'paper_id': paper_id}
        )
    else:
        # 显示所有的questions
        return render(request, 'questions/question_list.html', 
            {'pqrs': pqr_list, 'paper_id': paper_id}
        )
    
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
        POST : 提交答案
        GET : 显示问题
        url : ^question/(?P<pqr_id>[0-9]+)/$
    """
    pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    prev_pqr, next_pqr = pqr.arround_question()
    this_q = pqr.question
    if request.method == 'POST':
        # post请求
        form = this_q.get_answerform(request.POST)
        if form.is_valid(): # tips 需要先is_valid 后 cleaned_data
            answer = form.cleaned_data['answer']
        score, user_answer = this_q.check_answer(answer)
        pqr.score = score
        pqr.user_answer = user_answer
        pqr.save()
        if next_pqr:
            return redirect('questions:question_detail', next_pqr.id)
        else:
            return redirect('questions:paper_detail', pqr.paper.id)
    else:
        # get请求
        form = this_q.get_answerform()
        import markdown2
        return render(request, 'questions/question_detail.html', 
            {
                'pqr': pqr, 
                'next_pqr' : next_pqr,
                'prev_pqr' : prev_pqr,
                'form': form,
                "question_content": markdown2.markdown(this_q.problem)
            }
        )
    
def question_result(request, pqr_id):
    """ 
        显示具体question答案 
        url : ^question/(?P<pqr_id>[0-9]+)/result/$
    """
    pqr = PaperQuestionRelation.objects.get(pk = pqr_id)
    if pqr.paper.status != "DOING":
        # 只有不是 正在答题的 问卷才可以查看答案
        prev_pqr, next_pqr = pqr.arround_question()
        form = pqr.question.get_answerform()
        import markdown2
        return render(request, 'questions/question_result.html', 
            {
                'pqr': pqr, 
                'next_pqr' : next_pqr,
                'prev_pqr' : prev_pqr,
                'form': form,
                "question_content": markdown2.markdown(pqr.question.problem)
            }
        )
    else:
        return HttpResponse("请交卷后再查看答案")


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


