from __future__ import absolute_import
from django.contrib import admin

# Register your models here.
from .models import Employee, Payslip


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'active', 'send_email', 'cc_email']
    search_fields = ['name', 'email']


class PayslipAdmin(admin.ModelAdmin):
    list_display = ['employee', 'filename', 'date_release', 'created']
    search_fields = ['filename']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Payslip, PayslipAdmin)
