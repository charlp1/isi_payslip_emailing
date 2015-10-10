from django.db import models


class Employee(models.Model):

    name = models.CharField('Employee Name', max_length=1064, null=False)
    email = models.EmailField('Email')
    active = models.BooleanField('Is Active', default=False)
    send_email = models.BooleanField('Send Email', default=False)
    cc_email = models.EmailField('CC Email')

    def __str__(self):
        return self.name


class Payslip(models.Model):

    employee = models.ForeignKey(Employee)
    filename = models.FileField('Payslip Filename', default='')
    date_release = models.DateTimeField('Date Release', default=None)
    created = models.DateTimeField(auto_now=True)