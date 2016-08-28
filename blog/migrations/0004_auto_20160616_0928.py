# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=40, null=True, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='url',
            field=models.URLField(max_length=40, null=True, verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\xbd\x91\xe9\xa1\xb5\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
        ),
    ]
