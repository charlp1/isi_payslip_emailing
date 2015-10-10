# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payslip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='cc_email',
            field=models.EmailField(default='', max_length=254, verbose_name=b'CC Email'),
            preserve_default=False,
        ),
    ]
