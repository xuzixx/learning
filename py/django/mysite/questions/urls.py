#!/usr/bin/python
#-*- Encoding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # 登录
    url(r'^user_login/$', views.user_login, name = "user_login"),
    url(r'^user_logout/$', views.user_logout, name = "user_logout"),
    
    # 首页
    url(r'^paper/$', views.paper_index, name = "paper_index"),
    # 新建一个paper
    url(r'^paper/new/$', views.paper_new, name = 'paper_new'),
    # paper详细
    url(r'^paper/(?P<paper_id>[0-9]+)/$', views.paper_detail, name = 'paper_detail'),
    # paper结果
    #url(r'^paper/(?P<paper_id>[0-9]+)/result/$', views.paper_result, name = 'paper_result'),

    # question内容 !! pqr_id 不是question_id
    url(r'^question/(?P<pqr_id>[0-9]+)/$', views.question_detail, name = 'question_detail'),
    # question结果
    url(r'^question/(?P<pqr_id>[0-9]+)/result/$', views.question_result, name = 'question_result'),

    # test url
    url(r'^test/$', views.test, name = 'question_test'),
    url(r'^test_markdown/$', views.test_markdown, name = 'question_test_markdown'),
]


