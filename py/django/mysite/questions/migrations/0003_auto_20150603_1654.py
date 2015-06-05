# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150603_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionuser',
            name='content',
        ),
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default=b'TEST (2015-06-03)', max_length=250, verbose_name=b'\xe8\xaf\x95\xe5\x8d\xb7\xe6\xa0\x87\xe9\xa2\x98'),
        ),
        migrations.AlterField(
            model_name='page',
            name='questions',
            field=models.ManyToManyField(related_name='pages', through='questions.PageQuestionRelation', to='questions.Question'),
        ),
        migrations.AlterField(
            model_name='pagequestionrelation',
            name='page',
            field=models.ForeignKey(related_name='question_relations', to='questions.Page'),
        ),
        migrations.AlterField(
            model_name='pagequestionrelation',
            name='question',
            field=models.ForeignKey(related_name='page_relations', to='questions.Question'),
        ),
    ]
