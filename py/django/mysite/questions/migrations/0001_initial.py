# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=5, choices=[(b'SC', b'\xe5\x8d\x95\xe9\x80\x89\xe9\xa2\x98'), (b'MC', b'\xe5\xa4\x9a\xe9\x80\x89\xe9\xa2\x98'), (b'SA', b'\xe7\xae\x80\xe7\xad\x94\xe9\xa2\x98')])),
                ('content', models.CharField(max_length=250)),
            ],
        ),
    ]
