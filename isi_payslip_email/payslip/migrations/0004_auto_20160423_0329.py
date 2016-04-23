# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payslip', '0003_auto_20151114_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payslipfolder',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
