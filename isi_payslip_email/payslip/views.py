from __future__ import absolute_import

import re
from os.path import join
from datetime import date, timedelta
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.http import JsonResponse

from utils.api import GenericAPIView
from .forms import SendPayslipForm
from .models import Employee, Payslip, PayslipFolder


class Home(TemplateView):
    template_name = 'home.html'


class EmployeeView(TemplateView):
    template_name = 'employee_table.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['table'] = True

        make_emp = lambda u: {'id':u.id, 'name': u.name, 'email': u.email,
                               'active': u.active, 'send_email': u.send_email,
                               'cc_email': u.cc_email}

        if(self.request.GET.get('id')):
            id = int(self.request.GET.get('id'))
            pslips = Payslip.objects.filter(employee=id)
            context['payslips'] = []
            for p in pslips:
                context['payslips'].append({'name': p.filename.name, 'date': p.date_release})

            context['emp'] = {'name' : p.employee.name, 'email' : p.employee.email, 'active' : p.employee.active}
            context['table'] = False
        else:
            emp = Employee.objects.all()

            context['emp'] = [ make_emp(e) for e in emp ]

        return context




class PayslipSendView(FormView):
    template_name = 'payslip/index.html'
    template_name_sent = 'payslip/success_email_payslip.html'
    form_class = SendPayslipForm
    success_url = 'payslip/send/'

    def form_valid(self, form):
        employees = Employee.objects.filter(active=True, send_email=True)
        for employee in employees:
            form.send_payslip(employee)

        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }

        return self.response_class(**response_kwargs)


class PayslipUploadView(TemplateView):
    template_name = 'payslip/upload.html'

    def post(self, request):
        data = request.FILES['files[]']

        filename = data.name
        split_name = filename.split(settings.PAYSLIP_PATH_SEPARATOR)

        response = {
            'status': 'error',
            'filename': filename,
            'message': ''
        }
        check = True
        if not filename.endswith('.pdf'):
            check = False
            response.update({'message': 'Invalid File Format.'})

        if len(split_name) != 2:
            check = False
            response.update({'message': 'Invalid Filename Format.'})

        if check:
            pf_name = split_name[0].strip()
            e_name = re.sub('.pdf', '', split_name[1]).strip()

            try:
                employee = Employee.objects.get(name=e_name)
            except Employee.DoesNotExist:
                response.update({'message': 'No Employee Found.'})
            else:
                payslip_folder, created = PayslipFolder.objects.get_or_create(name=pf_name)

                precord = {'employee': employee, 'filename': data, 'payslip_folder': payslip_folder,
                           'date_release': datetime.now()}
                Payslip(**precord).save()
                payslip_folder.total_updloaded = Payslip.objects.filter(payslip_folder=payslip_folder).count()
                payslip_folder.save()
                response.update({'status': 'ok', 'message': 'success'})

        return JsonResponse(response)


class MissingUploadedEmployeeAPIView(GenericAPIView):

    allowed_methods = ['GET', ]

    def get(self, request, *args, **kwargs):
        response = {
            'status': 'error',
            'message': 'Request Invalid.',
            'data': {}
        }
        data = request.data
        pf_name = data.get('payslip', None)
        if pf_name:
            try:
                payslip_folder = PayslipFolder.objects.get(name=pf_name)
            except PayslipFolder.DoesNotExist:
                response.update({'message': 'No Payslip Found.'})
            else:
                employee_ids = Payslip.objects.values_list('employee_id').filter(payslip_folder=payslip_folder)
                employees = Employee.objects.filter(active=True, send_email=True).exclude(pk__in=employee_ids)
                response.update({'status': 'ok', 'message': 'success', 'data': [e.name for e in employees]})

        return JsonResponse(response)

def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)
