# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20150603_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(default=b'TEST (2015-06-03)', max_length=250, verbose_name=b'\xe8\xaf\x95\xe5\x8d\xb7\xe6\xa0\x87\xe9\xa2\x98')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
        migrations.CreateModel(
            name='PaperQuestionRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seq_num', models.IntegerField(verbose_name=b'\xe9\xa2\x98\xe7\x9b\xae\xe5\xba\x8f\xe5\x8f\xb7')),
                ('user_answer', models.CharField(max_length=500, verbose_name=b'\xe7\xad\x94\xe6\xa1\x88')),
                ('score', models.IntegerField(verbose_name=b'\xe5\xbe\x97\xe5\x88\x86')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('paper', models.ForeignKey(related_name='question_relations', to='questions.Paper')),
                ('question', models.ForeignKey(related_name='paper_relations', to='questions.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='page',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pagequestionrelation',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pagequestionrelation',
            name='question',
        ),
        migrations.AlterField(
            model_name='questionuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1'),
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='PageQuestionRelation',
        ),
        migrations.AddField(
            model_name='paper',
            name='questions',
            field=models.ManyToManyField(related_name='papers', through='questions.PaperQuestionRelation', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='paper',
            name='user',
            field=models.ForeignKey(related_query_name=b'paper', related_name='papers', to='questions.QuestionUser'),
        ),
    ]
