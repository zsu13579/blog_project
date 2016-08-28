# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_user_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(default=b'lvzq', max_length=30, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85'),
        ),
    ]
