# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
        migrations.CreateModel(
            name='PageQuestionRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer', models.CharField(max_length=500, verbose_name=b'\xe7\xad\x94\xe6\xa1\x88')),
                ('score', models.IntegerField(verbose_name=b'\xe5\xbe\x97\xe5\x88\x86')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('page', models.ForeignKey(to='questions.Page')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('email', models.CharField(max_length=250, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1')),
                ('content', models.CharField(max_length=250, verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe5\x86\x85\xe5\xae\xb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 16, 5, 9, 544418), verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 3, 16, 5, 22, 473119), verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.CharField(max_length=250, verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe5\x86\x85\xe5\xae\xb9'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=5, verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'SC', b'\xe5\x8d\x95\xe9\x80\x89\xe9\xa2\x98'), (b'MC', b'\xe5\xa4\x9a\xe9\x80\x89\xe9\xa2\x98'), (b'SA', b'\xe7\xae\x80\xe7\xad\x94\xe9\xa2\x98')]),
        ),
        migrations.AddField(
            model_name='pagequestionrelation',
            name='question',
            field=models.ForeignKey(to='questions.Question'),
        ),
        migrations.AddField(
            model_name='page',
            name='questions',
            field=models.ManyToManyField(to='questions.Question', through='questions.PageQuestionRelation'),
        ),
        migrations.AddField(
            model_name='page',
            name='user',
            field=models.ForeignKey(related_query_name=b'page', related_name='pages', to='questions.QuestionUser'),
        ),
    ]
