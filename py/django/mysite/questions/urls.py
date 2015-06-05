#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # 首页
    url(r'^paper/$', views.paper_index, name = "paper_index"),
    # 新建一个paper
    url(r'^paper/new/$', views.paper_new, name = 'paper_new'),
    # paper详细
    url(r'^paper/(?P<paper_id>[0-9]+)/$', views.paper_detail, name = 'paper_detail'),
    # paper结果
    url(r'^paper/(?P<paper_id>[0-9]+)/results/$', views.paper_results, name = 'paper_results'),
    # test url
    url(r'^test/$', views.test, name = 'question_test'),
]
