#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.shortcuts import render, render_to_response

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


# Create your views here.

def paper_index(request):
    paper_list = Paper.objects.order_by("-update_time")
    paginator = Paginator(paper_list,10)

    page = request.GET.get('page', 1)
    try:
        papers = paginator.page(page)
    except PageNotAnInteger:
        papers = paginator.page(1)
    except EmptyPage:
        papers = paginator.page(paginator.num_pages)
    return render_to_response('questions/paper_index.html', {'papers': papers})


def paper_new(request):
    pass

def paper_detail(request, paper_id):
    return HttpResponse(paper_id)

def paper_results(request, paper_id):
    return HttpResponse(paper_id)

def test(request):
    import markdown2
    return render_to_response('questions/README.md', 
            {"my_content": markdown2.markdown("**123**<br/>456")}
        )


