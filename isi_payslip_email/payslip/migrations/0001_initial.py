# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1064, verbose_name=b'Employee Name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('active', models.BooleanField(default=False, verbose_name=b'Is Active')),
                ('send_email', models.BooleanField(default=False, verbose_name=b'Send Email')),
            ],
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.FileField(default=b'', upload_to=b'', verbose_name=b'Payslip Filename')),
                ('date_release', models.DateTimeField(default=None, verbose_name=b'Date Release')),
                ('created', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(to='payslip.Employee')),
            ],
        ),
    ]
