# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('en_title', models.CharField(max_length=100, verbose_name='\u82f1\u6587\u6807\u9898')),
                ('img', models.CharField(default=b'/static/img/article/default.jpg', max_length=200)),
                ('tags', models.CharField(help_text='\u7528\u9017\u53f7\u5206\u9694\u5f00', max_length=200, null=True, verbose_name='\u6807\u7b7e', blank=True)),
                ('summary', models.TextField(verbose_name='\u6458\u8981')),
                ('content', models.TextField(verbose_name='\u6b63\u6587')),
                ('view_times', models.IntegerField(default=0)),
                ('zan_times', models.IntegerField(default=0)),
                ('is_top', models.BooleanField(default=False, verbose_name='\u7f6e\u9876')),
                ('rank', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(0, '\u6b63\u5e38'), (1, '\u8349\u7a3f'), (2, b'\xe5\x88\xa0\xe9\x99\xa4')])),
                ('pub_time', models.DateTimeField(default=False, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['rank', '-is_top', '-pub_time', '-create_time'],
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
    ]
