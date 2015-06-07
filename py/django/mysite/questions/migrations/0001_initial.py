# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('title', models.CharField(default=b'TEST (2015-06-07)', max_length=250, verbose_name=b'\xe8\xaf\x95\xe5\x8d\xb7\xe6\xa0\x87\xe9\xa2\x98')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaperQuestionRelation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('seq_num', models.IntegerField(verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe5\xba\x8f\xe5\x8f\xb7')),
                ('user_answer', models.CharField(max_length=500, verbose_name=b'\xe7\xad\x94\xe6\xa1\x88')),
                ('score', models.IntegerField(verbose_name=b'\xe5\xbe\x97\xe5\x88\x86')),
                ('paper', models.ForeignKey(related_name='question_relations', to='questions.Paper')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaperUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('email', models.EmailField(max_length=254, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('type', models.CharField(max_length=5, verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'SC', b'\xe5\x8d\x95\xe9\x80\x89\xe9\xa2\x98'), (b'MC', b'\xe5\xa4\x9a\xe9\x80\x89\xe9\xa2\x98'), (b'SA', b'\xe7\xae\x80\xe7\xad\x94\xe9\xa2\x98')])),
                ('title', models.CharField(max_length=250, verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe6\xa0\x87\xe9\xa2\x98')),
                ('problem', models.TextField(default=b'', verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae')),
                ('answer', models.CharField(default=b'', max_length=250, verbose_name=b'\xe7\xad\x94\xe6\xa1\x88')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionPic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('pic', models.ImageField(upload_to=b'questions/QuestionPic/%Y/%m/%d', blank=True)),
                ('question', models.ForeignKey(related_name='question_pics', to='questions.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='paperquestionrelation',
            name='question',
            field=models.ForeignKey(related_name='paper_relations', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='paper',
            name='questions',
            field=models.ManyToManyField(related_name='papers', through='questions.PaperQuestionRelation', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='paper',
            name='user',
            field=models.ForeignKey(related_query_name=b'paper', related_name='papers', to='questions.PaperUser'),
        ),
    ]
