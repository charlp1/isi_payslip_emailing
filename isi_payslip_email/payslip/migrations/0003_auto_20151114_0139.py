# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import payslip.models


class Migration(migrations.Migration):

    dependencies = [
        ('payslip', '0002_employee_cc_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayslipFolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1064)),
                ('created', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('total_uploaded', models.IntegerField(default=0)),
                ('total_sent', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='payslip',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='filename',
            field=models.FileField(default=b'', upload_to=payslip.models.upload_payslip_holder, verbose_name=b'Payslip Filename'),
        ),
        migrations.AddField(
            model_name='payslip',
            name='payslip_folder',
            field=models.ForeignKey(to='payslip.PayslipFolder'),
            preserve_default=False,
        ),
    ]
