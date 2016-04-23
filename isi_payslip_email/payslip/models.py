import os
from django.db import models
from django.core.files.storage import FileSystemStorage


class OverwritePayslipStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwritePayslipStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name


def upload_payslip_holder(model_instance, filename):
    return os.path.join(model_instance.payslip_folder.name, filename)



class Employee(models.Model):

    name = models.CharField('Employee Name', max_length=1064, null=False)
    email = models.EmailField('Email')
    active = models.BooleanField('Is Active', default=False)
    send_email = models.BooleanField('Send Email', default=False)
    cc_email = models.EmailField('CC Email')

    def __str__(self):
        return self.name


class PayslipFolder(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    created = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    total_uploaded = models.IntegerField(default=0)
    total_sent = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Payslip(models.Model):

    employee = models.ForeignKey(Employee)
    payslip_folder = models.ForeignKey(PayslipFolder)
    filename = models.FileField('Payslip Filename', default='', upload_to=upload_payslip_holder,
                                storage=OverwritePayslipStorage())
    status = models.BooleanField(default=False)
    date_release = models.DateTimeField('Date Release', default=None)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.name
